# BaseHTTPRequestHandler — це клас, який вміє:
# - приймати HTTP-запити
# - розбирати headers, method, path
# - дозволяє нам перевизначати методи do_GET, do_POST і т.д.
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Це "база даних" для нашого першого сервера
# Зараз це просто список у памʼяті
# Кожна задача — словник (dict)
tasks = [
    {"id": 1, "title": "Learn HTTP"},
    {"id": 2, "title": "Write backend"}
]

# Створюємо власний handler
# Handler — це клас, який буде:
# - створюватися для КОЖНОГО HTTP-запиту
# - обробляти конкретний запит (GET, POST і т.д.)
class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):

        # self.path — це URL-шлях, який прийшов у запиті
        # Наприклад:
        # GET /tasks HTTP/1.1
        # self.path == "/tasks"
        if self.path == "/tasks":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("X-Powered-By", "Python")

            # Повідомляємо серверу:
            # "Заголовки закінчилися, далі піде тіло відповіді"
            self.end_headers()
            response_data ={
                "tasks": tasks
            }
            # json.dumps(tasks):
            #   - перетворює Python list -> JSON string
            # .encode():
            #   - HTTP працює з байтами, а не з рядками
            # self.wfile.write():
            #   - відправляє тіло відповіді клієнту
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
        if self.path == "/tasks":
            try:
                #1 Визначаємо розмір вхідних даних
                # Header 'Content-Length' визначає скільки байтів прислав клієнт 
                content_length = int(self.headers.get('Content-Length', 0)) 

                #2 Читаємо тіло запиту
                # self.rfile (read file) - це потік вхідних байтів
                raw_data = self.rfile.read(content_length)

                #3 Декодуємо байти в рядок та парсимо JSON
                data = json.loads(raw_data.decode('utf-8'))
                
                #4 Валідація даних
                if "title" not  in data:
                    # Якщо немає поля title - це помилка клієнта
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Title is required"}).encode())
                    return
                
                for task in tasks:
                    if task["title"] == data["title"]:
                        self.send_response(409)
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": "Task already exists"}).encode())
                        return
                
                if not (isinstance(data["title"], str)):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Title should be string"}).encode())
                    return

                #5 Створю нову задачу
                new_task = {
                    "id": len(tasks) + 1,
                    "title": data["title"]
                }
                tasks.append(new_task)

                #6 Відправляємо успішну відповідь
                #201 = Created (стандарт для успішного створення ресурсу)
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                # Повертаємо клієнту об'єкт, який ми створили(з новими ID)
                self.wfile.write(json.dumps(new_task).encode())

            except json.JSONDecodeError:
                # Якщо клієнт прислав не JSON
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())

            except Exception as e:
                # На випадок інших непередбачуваних помилок 
                self.send_response(500) # Internal Server Error
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
        
if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    print("Server started at http://localhost:8000")
    server.serve_forever()