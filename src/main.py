import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Настройка порта и хоста
PORT = 8000
HOST = "127.0.0.1"


class ContactsWebhookHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обрабатывает абсолютно любой GET-запрос и возвращает HTML."""
        # 1. Формируем путь к файлу контактов относительно расположения скрипта
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_html = os.path.join(current_dir, "templates", "contacts.html")

        try:
            # 2. Читаем содержимое HTML-файла (используем utf-8 для корректного отображения кириллицы)
            with open(path_to_html, "r", encoding="utf-8") as file:
                html_content = file.read()

            # 3. Отправляем успешный статус ответа сервера (200 OK)
            self.send_response(200)

            # 4. Устанавливаем заголовок text/html взамен application/json
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # 5. Переводим строку в байты и отправляем пользователю в браузер
            self.wfile.write(bytes(html_content, "utf-8"))


        except FileNotFoundError:

            self.send_response(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            error_message = "Ошибка: Файл templates/contacts.html не найден."
            self.wfile.write(error_message.encode('utf-8'))

def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, ContactsWebhookHandler)
    print(f"Сервер успешно запущен! Откройте в браузере: http://{HOST}:{PORT}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
