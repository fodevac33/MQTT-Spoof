import paho.mqtt.client as mqtt
import socket
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import sqlite3
from datetime import datetime

# Get local IP address
ip = socket.gethostbyname(socket.gethostname())

# Database setup
DB_NAME = "data.db"

def insert_data(value):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO sensor_data (value, timestamp) VALUES (?, ?)",
              (value, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_latest_data(limit=20):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT value, timestamp FROM sensor_data ORDER BY id DESC LIMIT ?", (limit,))
    data = c.fetchall()
    conn.close()
    return [{"value": row[0], "timestamp": row[1]} for row in reversed(data)]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic} Received: {msg.payload.decode()}")
    try:
        value = float(msg.payload.decode())
        insert_data(value)
    except ValueError:
        print(f"Invalid data received: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# HTTP server to handle GET requests from the frontend
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = get_latest_data()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def end_headers(self):
        super().end_headers()

def run_http_server():
    server_address = ('0.0.0.0', 8000)  
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"HTTP server running on http://{ip}:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=run_http_server)
    http_thread.start()

    # Connect and start MQTT client
    client.connect(ip, 1883, 60)
    client.loop_forever()
