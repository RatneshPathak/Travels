#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 3000
DIRECTORY = "/app/frontend"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"Serving frontend at http://0.0.0.0:{PORT}")
    print(f"Directory: {DIRECTORY}")
    httpd.serve_forever()
