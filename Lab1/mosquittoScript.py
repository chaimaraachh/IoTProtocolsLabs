import paho.mqtt.client as paho
import time

broker = "rt" 
port = 8883
conn_flag = False

def on_connect(client, userdata, flags, rc):
    global conn_flag
    if rc == 0:
        conn_flag = True
        print("Connected successfully")
        # Publish 10 messages when connected
        for i in range(1, 3):
            message = "Message {} from Windows with TLS".format(i)
            client.publish("test/topic", message)
            print("Sent:", message)
            time.sleep(1)  # Wait 1 second between messages
    else:
        print("Connection failed with code", rc)

def on_log(client, userdata, level, buf):
    print("Log: ", buf)

def on_disconnect(client, userdata, rc):
    print("Client disconnected with code", rc)

client1 = paho.Client("control1")
client1.on_log = on_log
client1.on_connect = on_connect
client1.on_disconnect = on_disconnect

client1.tls_set('ca.crt', tls_version=paho.ssl.PROTOCOL_TLSv1_2)
client1.tls_insecure_set(True)  

client1.connect(broker, port)

client1.loop_start()

time.sleep(15)

client1.loop_stop()
client1.disconnect()
