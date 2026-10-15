#!/usr/bin/env python3
import json, os, sys
from http.server import HTTPServer, BaseHTTPRequestHandler

FEEDBACK_FILE = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit/storyboard_feedback.json'

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode('utf-8'))
            with open(FEEDBACK_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok", "saved": true}')
        except Exception as e:
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(f'{{"error": "{str(e)}"}}\''.encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.wfile.write(b'{"scenes": []}')

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8765), Handler)
    print("Storyboard sync server running on http://127.0.0.1:8765")
    server.serve_forever()
