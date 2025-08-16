print("Hello from Railway!")
print("Test file is working!")

import os
print(f"PORT: {os.environ.get('PORT', 'NOT SET')}")
print(f"Current directory: {os.getcwd()}")
print(f"Files: {os.listdir('.')}")

# Simple HTTP server
from http.server import HTTPServer, BaseHTTPRequestHandler

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"TEST OK")

port = int(os.environ.get("PORT", 8000))
print(f"Starting server on port {port}")

server = HTTPServer(('0.0.0.0', port), TestHandler)
print("Server started!")
server.serve_forever() 