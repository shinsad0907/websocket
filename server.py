import asyncio
import websockets
import json
from flask import Flask, jsonify

app = Flask(__name__)

# WebSocket server handler
clients = set()

async def echo(websocket, path):
    # Thêm client vào danh sách khi kết nối
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
    finally:
        # Xóa client khỏi danh sách khi ngắt kết nối
        clients.remove(websocket)

# Hàm gửi tin nhắn từ file tới tất cả các client
async def send_message_from_file():
    while True:
        try:
            with open("message.txt", "r") as file:
                message = file.read()
            for client in clients:
                if client.open:
                    await client.send(message)
            await asyncio.sleep(10)  # Gửi tin nhắn mỗi 10 giây
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)

# Chạy WebSocket server trong một background task
async def start_websocket_server():
    server = await websockets.serve(echo, "0.0.0.0", 8765)
    await send_message_from_file()
    await server.wait_closed()

# Đường dẫn Flask
@app.route('/')
def index():
    return jsonify({"message": "WebSocket server is running"})

if __name__ == '__main__':
    # Chạy Flask server và WebSocket server đồng thời
    loop = asyncio.get_event_loop()
    loop.create_task(start_websocket_server())
    app.run(host='0.0.0.0', port=5000)
