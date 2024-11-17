import paho.mqtt.client as mqtt
import time
import random
import math

# Configuration
broker = "192.168.116.139"  # VM as broker
pc_broker = "192.168.1.1"  # Edgebroker IP for response
port = 1883
data_topic = "sensor/data"
mean_topic = "sensor/mean_data"
received_data = []

# Parameter for Poisson-distributed intervals
lambda_rate = 2  # Average rate for the Poisson interval (events per second)

# Callback function to receive and store data
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(data_topic)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    data = float(msg.payload.decode())
    print(f"Received data: {data}")
    received_data.append(data)

# Function to calculate Poisson interval
def next_time_interval(l):
    n = random.random()
    inter_event_time = -math.log(1.0 - n) / l
    return inter_event_time

# Function to calculate and publish the mean
def publish_mean(mean_value):
    response_client = mqtt.Client("VM_Publisher")
    response_client.connect(pc_broker, port)
    response_client.publish(mean_topic, str(mean_value))
    response_client.disconnect()
    print(f"Published mean value: {mean_value}")

# Function to calculate mean of collected data
def calculate_mean(data):
    return sum(data) / len(data) if data else None

# Main function for managing Poisson intervals, collection, and publishing
def collect_and_publish_mean():
    global received_data

    while True:
        # Collect data for a Poisson-distributed interval
        interval = next_time_interval(lambda_rate)
        print(f"Collecting data for the next {interval:.2f} seconds...")
        time.sleep(interval)

        # Calculate mean of collected data
        if received_data:
            mean_value = calculate_mean(received_data)
            publish_mean(mean_value)
            received_data = []  # Clear data after publishing
        else:
            print("No data received in this interval to calculate mean.")

# MQTT client setup to receive data
client = mqtt.Client("VM_Receiver")
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker and start receiving loop
client.connect(broker, port)
client.loop_start()

try:
    # Start the data collection and publishing loop
    collect_and_publish_mean()
except KeyboardInterrupt:
    print("Stopping receiver...")

client.loop_stop()
client.disconnect()
