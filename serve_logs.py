#!/usr/bin/env python3
"""
Simple HTTP server to serve the log viewer and API logs
Run this to view logs in your browser
"""

import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("="*60)
        print(f"🌐 Log Viewer Server Started")
        print("="*60)
        print(f"\n📍 Open in browser: http://localhost:{PORT}/view_logs.html")
        print(f"📂 Serving from: {DIRECTORY}")
        print(f"\n⚡ Press Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✋ Server stopped. Goodbye!")

if __name__ == "__main__":
    main()

