import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt

# Configuration
broker = "192.168.1.1"  # Edge broker
port = 1883
mean_topic = "sensor/mean_data"

# Data storage for plotting
mean_values = []
timestamps = []

# Callback function to handle incoming mean data
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(mean_topic)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    mean_value = float(msg.payload.decode())
    print(f"Received mean value: {mean_value}")
    mean_values.append(mean_value)  # Store mean value
    timestamps.append(time.time())  # Record the timestamp

# MQTT client setup for receiving mean data
client = mqtt.Client("PC_Receiver")
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker and start loop
client.connect(broker, port)
client.loop_start()

try:
    print("Press Ctrl+C to stop.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping receiver...")

# Stop MQTT loop
client.loop_stop()
client.disconnect()

if timestamps:
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]

# Plot the mean values in a stem plot
if mean_values:
    plt.figure(figsize=(10, 5))
    plt.stem(timestamps, mean_values, label="Received Mean Values")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Mean Value")
    plt.title("Mean Data Received Over Time")
    plt.legend()
    plt.show()
else:
    print("No data received to plot.")
