from http.server import BaseHTTPRequestHandler, HTTPServer
import json

items = [
    {"id": 1, "title": "Learn HTTP"},
    {"id": 2, "title": "Write backend"}
]


class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/items":
            self.send_response(200)

            self.send_header("Content-Type", "application/json")
            self.send_header("X-Powered-By", "Python")
            self.end_headers()

            response_data ={
                "tasks": items
            }
            self.wfile.write(json.dumps(response_data).encode())

        elif self.path =="/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()


            response_data ={
                "message": "API is running"
            }
            self.wfile.write(json.dumps(response_data).encode())

        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        self.send_response(405)
        self.end_headers()

server = HTTPServer(("localhost", 8000), Handler)
server.serve_forever()