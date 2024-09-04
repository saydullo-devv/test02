
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from database import DatabaseManager  # To'g'ridan-to'g'ri import nisbiy importni o'rniga

# Ma'lumotlar bazasi menejerini ishga tushirish
db_manager = DatabaseManager("todo.db")


class TodoHTTPRequestHandler(BaseHTTPRequestHandler):
    """Todo HTTP so'rovlarini boshqarish uchun handler."""

    def set_headers(self, status=200):
        """Javob sarlavhalarini o'rnatish."""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """GET so'rovlarini qayta ishlash."""
        if self.path == '/':
            self.set_headers()
            todos = db_manager.get_all()  # Ushbu metod DatabaseManager'da mavjudligiga ishonch hosil qiling
            self.wfile.write(json.dumps(todos).encode())
        else:
            self.send_error(404, message="Page not found")  # Agar URL noto'g'ri bo'lsa, 404 qaytaring

    def do_POST(self):
        """POST so'rovlarini qayta ishlash."""
        if self.path == '/create-todo':
            content_length = int(self.headers['Content-Length'])  # O'zgaruvchi nomini to'g'rilash
            post_data = self.rfile.read(content_length)
            todo_item = json.loads(post_data.decode())

            if 'task' in todo_item and 'completed' in todo_item:
                db_manager.create_todo(
                    todo_item['task'], todo_item['completed'])
                self.set_headers(201)
                self.wfile.write(json.dumps(todo_item).encode())
            else:
                self.send_error(400, message="Bad Request: 'task' or 'completed' fields missing")
        else:
            self.send_error(404, message="Page not found")

    def do_PUT(self):
        """PUT so'rovlarini qayta ishlash."""
        if self.path.startswith('/todo/'):
            todo_id = int(self.path.split('/')[-1])
            content_length = int(self.headers['Content-Length'])  # O'zgaruvchi nomini to'g'rilash
            put_data = self.rfile.read(content_length)
            todo_item = json.loads(put_data.decode())

            if 'task' in todo_item and 'completed' in todo_item:
                db_manager.update_todo(
                    todo_id, todo_item['task'], todo_item['completed']
                )
                self.set_headers(200)
            else:
                self.send_error(400, message="Bad Request: 'task' or 'completed' fields missing")
        else:
            self.send_error(404, message="Page not found")

    def do_DELETE(self):
        """DELETE so'rovlarini qayta ishlash."""
        if self.path.startswith('/todo/'):
            todo_id = int(self.path.split('/')[-1])
            db_manager.delete_todo(todo_id)
            self.set_headers(204)
        else:
            self.send_error(404, message="Page not found")


def run(server_class=HTTPServer, handler_class=TodoHTTPRequestHandler):
    """HTTP serverni ishga tushirish."""
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Server 8000 portda ishga tushmoqda...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()



