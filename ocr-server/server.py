#!/usr/bin/env python3
"""Server OCR lokal untuk tab "PDF → Markdown" di PDF Combine.

Aplikasi web (index.html) merender halaman PDF menjadi gambar di browser, lalu
mengirimkannya ke server ini. Server menjalankan model Unlimited-OCR 2
(https://github.com/baidu/Unlimited-OCR) dan mengembalikan keluaran mentah model
(blok <PAGE><BLOCK>...). Konversi ke Markdown dilakukan di browser.

Backend:
  transformers  (bawaan) memuat baidu/Unlimited-OCR-2 langsung di GPU NVIDIA.
  sglang        meneruskan permintaan ke server SGLang resmi (Linux, GPU besar).
  demo          tanpa model: mengembalikan contoh keluaran untuk mencoba antarmuka.

Contoh:
  python server.py                       # transformers, http://127.0.0.1:8000
  python server.py --backend sglang --sglang-url http://127.0.0.1:10000
  python server.py --backend demo

API:
  GET  /health -> {"ok": true, "backend": "...", "model": "...", "ready": true}
  POST /ocr    {"images": ["data:image/jpeg;base64,..."], "crop_mode": true|false|null}
            -> {"text": "<PAGE><BLOCK>...", "pages": n, "seconds": t}
"""
import argparse
import base64
import contextlib
import io
import json
import os
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MAX_BODY = 512 * 1024 * 1024  # 512 MB
PAGE_TOKEN = '<PAGE>'
VERBOSE = False  # --verbose: tampilkan log debug bawaan kode model


def log(msg):
    """Pesan server; selalu tampil walau stdout model sedang dibisukan."""
    sys.__stdout__.write(msg + '\n')
    sys.__stdout__.flush()


@contextlib.contextmanager
def quiet():
    """Bisukan print() debug dari kode model ([PageRope], [DASH], ...) kecuali --verbose."""
    if VERBOSE:
        yield
        return
    with open(os.devnull, 'w', encoding='utf-8') as sink, contextlib.redirect_stdout(sink):
        yield


def decode_image(item):
    """Data URL / base64 -> PIL.Image (RGB)."""
    from PIL import Image
    if not isinstance(item, str) or not item:
        raise ValueError('gambar kosong')
    b64 = item.split(',', 1)[1] if item.startswith('data:') else item
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGB')


def normalize_pages(text, n_pages):
    """Pastikan keluaran diawali <PAGE> agar penomoran halaman di browser tidak bergeser."""
    text = text or ''
    if n_pages and PAGE_TOKEN not in text[:64]:
        text = PAGE_TOKEN + text
    return text


# ── Backends ────────────────────────────────────────────────────────────────
class TransformersBackend:
    name = 'transformers'

    def __init__(self, model_name):
        import torch
        from transformers import AutoModel, AutoTokenizer
        if not torch.cuda.is_available():
            raise SystemExit(
                'CUDA tidak tersedia. Unlimited-OCR 2 membutuhkan GPU NVIDIA dan PyTorch versi CUDA.\n'
                'Pasang PyTorch CUDA dari https://pytorch.org/get-started/locally/ atau jalankan '
                'dengan --backend demo untuk mencoba antarmuka.')
        self.model_name = model_name
        log(f'[ocr] Memuat {model_name} ke {torch.cuda.get_device_name(0)} ...')
        with quiet():
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            self.model = AutoModel.from_pretrained(
                model_name, trust_remote_code=True, use_safetensors=True,
                torch_dtype=torch.bfloat16).eval().cuda()
        self.torch = torch
        log('[ocr] Model siap.')

    def ocr(self, images, crop_mode):
        pil = [decode_image(x) for x in images]
        try:
            with quiet():
                text = self.model.infer(
                    self.tokenizer,
                    image_file=pil if len(pil) > 1 else pil[0],
                    crop_mode=crop_mode,          # None = otomatis (gundam utk 1 halaman, base utk banyak)
                    eval_mode=True,               # jangan streaming ke stdout
                    no_repeat_ngram_size=35,      # sama dengan setelan evaluasi resmi
                    ngram_window=1024 if len(pil) > 1 else 128,
                )
        finally:
            self.torch.cuda.empty_cache()
        return text


class SGLangBackend:
    name = 'sglang'

    def __init__(self, url, model_name):
        import requests
        self.url = url.rstrip('/')
        self.model_name = model_name
        self.session = requests.Session()
        self.session.trust_env = False
        try:
            from sglang.srt.sampling.custom_logit_processor import DeepseekOCRNoRepeatNGramLogitProcessor
            self.ngram = DeepseekOCRNoRepeatNGramLogitProcessor.to_str()
        except Exception:
            self.ngram = None
            log('[ocr] Peringatan: sglang tidak terpasang di lingkungan ini; '
                'n-gram logit processor tidak dipakai.')

    def ocr(self, images, crop_mode, tokens_per_page=8000):
        n = len(images)
        urls = [x if x.startswith('data:') else 'data:image/jpeg;base64,' + x for x in images]
        content = [{'type': 'image_url', 'image_url': {'url': u}} for u in urls]
        content.append({'type': 'text', 'text': '<PAGE><image>' * n + 'Multi page parsing.'})
        payload = {
            'model': self.model_name,
            'messages': [{'role': 'user', 'content': content}],
            'max_tokens': tokens_per_page * n,
            'temperature': 0,
            'skip_special_tokens': False,
            'images_config': {'crop_mode': bool(crop_mode) if crop_mode is not None else n == 1},
        }
        if self.ngram:
            payload['custom_logit_processor'] = self.ngram
            payload['custom_params'] = {
                'ngram_size': 35, 'window_size': 1024 if n > 1 else 128,
                'page_token_id': 128827, 'eos_token_id': 1, 'max_page_tokens': 20000,
            }
        r = self.session.post(f'{self.url}/v1/chat/completions', json=payload, timeout=6000)
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']


class DemoBackend:
    name = 'demo'
    model_name = 'demo (tanpa model)'

    def ocr(self, images, crop_mode):
        time.sleep(0.6 * len(images))
        out = []
        for i, _ in enumerate(images):
            out.append(
                '<PAGE><BLOCK>title<LEVEL1>[80,40,920,80]<FORK>Contoh Keluaran OCR\n'
                '<BLOCK>text[80,100,920,180]<FORK>Ini adalah keluaran <b>demo</b> untuk halaman '
                f'ke-{i + 1} dalam permintaan ini. Jalankan server tanpa --backend demo untuk OCR sungguhan.\n'
                '<BLOCK>title<LEVEL2>[80,200,920,230]<FORK>Tabel\n'
                '<BLOCK>table[80,240,920,400]<FORK><table><tr><td>No</td><td>Nama</td><td>Nilai</td></tr>'
                '<tr><td>1</td><td>Andi</td><td>90</td></tr><tr><td>2</td><td>Budi</td><td>85</td></tr></table>\n'
                '<BLOCK>image[80,420,500,700]<FORK>\n'
                '<BLOCK>image_caption[80,705,500,730]<FORK>Gambar 1. Potongan area halaman.\n'
                '<BLOCK>equation[80,750,920,790]<FORK>$$E = mc^2$$\n'
                '<BLOCK>page_number[480,950,520,970]<FORK>' + str(i + 1))
        return ''.join(out)


# ── HTTP ────────────────────────────────────────────────────────────────────
def make_handler(backend, lock):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'UnlimitedOCRBridge/1.0'

        def _cors(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            # Chrome Private Network Access: izinkan halaman https (mis. GitHub Pages) memanggil localhost
            self.send_header('Access-Control-Allow-Private-Network', 'true')

        def _json(self, code, obj):
            body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
            self.send_response(code)
            self._cors()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self):
            self.send_response(204)
            self._cors()
            self.send_header('Content-Length', '0')
            self.end_headers()

        def do_HEAD(self):
            self.send_response(200)
            self._cors()
            self.send_header('Content-Length', '0')
            self.end_headers()

        def do_GET(self):
            if self.path.rstrip('/') in ('', '/health'):
                return self._json(200, {'ok': True, 'backend': backend.name,
                                        'model': backend.model_name, 'busy': lock.locked()})
            self._json(404, {'error': 'tidak ditemukan'})

        def do_POST(self):
            if self.path.rstrip('/') != '/ocr':
                return self._json(404, {'error': 'tidak ditemukan'})
            try:
                length = int(self.headers.get('Content-Length') or 0)
                if length <= 0 or length > MAX_BODY:
                    return self._json(413, {'error': 'ukuran permintaan tidak valid'})
                req = json.loads(self.rfile.read(length))
                images = req.get('images') or []
                if not images:
                    return self._json(400, {'error': 'images kosong'})
                crop_mode = req.get('crop_mode')
                if crop_mode not in (True, False, None):
                    crop_mode = None
                t0 = time.time()
                log(f'[ocr] Memproses {len(images)} halaman ...')
                with lock:  # satu GPU: proses permintaan satu per satu
                    text = backend.ocr(images, crop_mode)
                dt = time.time() - t0
                log(f'[ocr] {len(images)} halaman selesai dalam {dt:.1f} dtk')
                self._json(200, {'text': normalize_pages(text, len(images)),
                                 'pages': len(images), 'seconds': round(dt, 2)})
            except Exception as e:  # noqa: BLE001
                traceback.print_exc()
                self._json(500, {'error': f'{type(e).__name__}: {e}'})

        def log_message(self, fmt, *args):
            msg = fmt % args
            if '/health' not in msg and 'OPTIONS' not in msg:
                sys.stderr.write('[http] ' + msg + '\n')

    return Handler


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--backend', choices=['transformers', 'sglang', 'demo'], default='transformers')
    ap.add_argument('--model', default='baidu/Unlimited-OCR-2', help='ID model HuggingFace atau folder lokal')
    ap.add_argument('--sglang-url', default='http://127.0.0.1:10000')
    ap.add_argument('--sglang-model', default='Unlimited-OCR-2', help='--served-model-name pada server SGLang')
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=8000)
    ap.add_argument('--verbose', action='store_true', help='tampilkan log debug bawaan kode model')
    args = ap.parse_args()
    global VERBOSE
    VERBOSE = args.verbose

    if args.backend == 'transformers':
        backend = TransformersBackend(args.model)
    elif args.backend == 'sglang':
        backend = SGLangBackend(args.sglang_url, args.sglang_model)
    else:
        backend = DemoBackend()

    httpd = ThreadingHTTPServer((args.host, args.port), make_handler(backend, threading.Lock()))
    log(f'[ocr] Server {backend.name} berjalan di http://{args.host}:{args.port}  (Ctrl+C untuk berhenti)')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log('\n[ocr] Berhenti.')


if __name__ == '__main__':
    main()
