from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Сховище задач
tasks = [
    {"id": 1, "title": "Learn HTTP"},
    {"id": 2, "title": "Write backend"}
]

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Перевіряємо endpoint
        if self.path != "/tasks":
            self.send_response(404)
            self.end_headers()
            return

        # Отримуємо довжину body
        content_length = int(self.headers.get("Content-Length", 0))

        # Читаємо body(байти) Перетворюємо байти в рядок
        body_bytes = self.rfile.read(content_length)
        body_str = body_bytes.decode("utf-8")

        # Парсимо JSON
        try:
            data = json.loads(body_str)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        # Отримуємо title з JSON
        title = data.get("title")
        if not title:
            self.send_response(400)
            self.end_headers()
            return

        # Створюємо нову задачу
        new_task = {
            "id": len(tasks) +1,
            "title": title
        }

        # Додаємо задачу в список
        tasks.append(new_task)

         # Формуємо відповідь
        response = json.dumps(new_task)

        # Відправляємо відповідь клієнту
        self.send_response(201) #Created
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

# Запуск сервера 
server = HTTPServer(("localhost", 8000), Handler)
print("Server running on http://localhost:8000")
server.serve_forever()