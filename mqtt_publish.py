import time
import random
import paho.mqtt.client as mqtt

# MQTT Broker address and topic
broker_address = "172.26.10.16"
topic = "test/topic"

# Create an MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker_address)

# Function to publish data with random noise
def publish_data():
    # Generate a random value with noise
    value = 20 + 3*random.uniform(-1, 1)  # Adding random noise between -1 and 1

    # Limit value to 2 decimal points
    value_formatted = "{:.2f}".format(value)

    # Publish the formatted value to the MQTT topic
    client.publish(topic, value_formatted)

    # Print the published value (optional)
    print(f"Published: {value_formatted}")

# Main loop to publish data every second
try:
    while True:
        publish_data()
        time.sleep(2)  # Wait for 1 second;

except KeyboardInterrupt:
    print("\nProgram terminated by user.")

finally:
    client.disconnect()
