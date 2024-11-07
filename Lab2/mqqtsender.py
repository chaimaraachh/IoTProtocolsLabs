import time
import paho.mqtt.client as mqtt

# MQTT Variables
hostname = 'picoiothub.azure-devices.net'
clientid = 'picow'
username = 'picoiothub.azure-devices.net/picow/?api-version=2021-04-12'
password = 'SharedAccessSignature sr=picoiothub.azure-devices.netEXAMPLE'
topic_pub = 'devices/picow/messages/events/'
topic_msg = '{"buttonpressed":"1"}'
port_no = 8883  # Typically 8883 for MQTT over SSL
subscribe_topic = "devices/picow/messages/devicebound/#"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(subscribe_topic)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

def mqtt_connect():
    client = mqtt.Client(client_id=clientid)
    client.username_pw_set(username=username, password=password)

    # Disable SSL certificate verification
    client.tls_set(certfile=None, keyfile=None, cert_reqs=mqtt.ssl.CERT_NONE)
    client.tls_insecure_set(True)  # Disable strict SSL certificate verification

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(hostname, port_no, keepalive=60)
    return client

try:
    client = mqtt_connect()
    client.loop_start()

    while True:
        # Simulate button press
        client.publish(topic_pub, topic_msg)
        print(f"Published: {topic_msg}")
        time.sleep(5)  # Publish every 5 seconds

except KeyboardInterrupt:
    print("Disconnecting...")
    client.loop_stop()
    client.disconnect()
