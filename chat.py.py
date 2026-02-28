import flet as ft
import socket
import threading
import time

def main(page: ft.Page):
    page.title = "Чат"
    page.theme_mode = "ft.ThemeMode.DARK"
    page.scroll = "always"
    
    # Создаем элементы интерфейса
    chat_log = ft.Column(spacing=10, scroll="auto")
    message_input = ft.TextField(hint_text="Введите сообщение", expand=True)
    status = ft.Text("Подключение...")
    
    # Добавляем все на страницу
    page.add(
        status,
        ft.Container(
            content=chat_log,
            height=400,
            bgcolor=ft.Colors.BLACK12,  # ← ИСПРАВЛЕНО: ft.Colors.BLACK12
            padding=10
        ),
        ft.Row([message_input, ft.ElevatedButton("Отправить", on_click=lambda _: send_message())])
    )
    
    # Подключаемся к серверу
    try:
        client = socket.socket()
        client.connect(('192.168.0.18', 9999))
        status.value = "✅ Подключено"
        page.update()
    except Exception as e:
        status.value = f"❌ Ошибка: {e}"
        page.update()
        return
    
    def send_message():
        """Отправка сообщения"""
        if message_input.value:
            try:
                msg = message_input.value
                client.send(msg.encode())
                
                # Показываем наше сообщение
                chat_log.controls.append(ft.Text(f"Я: {msg}", color=ft.Colors.GREEN))
                message_input.value = ""
                page.update()
            except Exception as e:
                chat_log.controls.append(ft.Text(f"Ошибка: {e}", color=ft.Colors.RED))
                page.update()
    
    def receive_messages():
        """Получение сообщений в отдельном потоке"""
        while True:
            try:
                data = client.recv(1024)
                if data:
                    # Добавляем сообщение в лог
                    chat_log.controls.append(ft.Text(f"Друг: {data.decode()}", color=ft.Colors.BLUE))
                    page.update()  # Обновляем интерфейс
            except:
                break
            time.sleep(0.1)
    
    # Запускаем поток для получения сообщений
    thread = threading.Thread(target=receive_messages, daemon=True)
    thread.start()

if __name__ == "__main__":
    ft.app(target=main)