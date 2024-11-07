import time
import random  # Import random module to generate random temperatures
import paho.mqtt.client as mqtt

# MQTT Variables
hostname = 'picoiothub.azure-devices.net'
clientid = 'picow'
username = 'picoiothub.azure-devices.net/picow/?api-version=2021-04-12'
password = 'SharedAccessSignature sr=picoiothub.azure-devices.netEXAMPLE'
topic_pub = 'devices/picow/messages/events/'
port_no = 8883  # Typically 8883 for MQTT over SSL
subscribe_topic = "devices/picow/messages/devicebound/#"
certificate_path = "baltimore.pem"  # Path to Baltimore CA certificate

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(subscribe_topic)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

def mqtt_connect():
    client = mqtt.Client(client_id=clientid)
    client.username_pw_set(username=username, password=password)

    # Enable SSL with Baltimore certificate
    client.tls_set(ca_certs=certificate_path)
    client.tls_insecure_set(False)  # Enforce strict SSL certificate verification

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(hostname, port_no, keepalive=60)
    return client

try:
    client = mqtt_connect()
    client.loop_start()

    while True:
        # Generate a random temperature between a chosen range, e.g., 20-30 degrees Celsius
        random_temp = round(random.uniform(20, 30), 2)
        topic_msg = f'{{"temperature": "{random_temp}"}}'

        # Publish the temperature reading
        client.publish(topic_pub, topic_msg)
        print(f"Published: {topic_msg}")
        time.sleep(5)  # Publish every 5 seconds

except KeyboardInterrupt:
    print("Disconnecting...")
    client.loop_stop()
    client.disconnect()
