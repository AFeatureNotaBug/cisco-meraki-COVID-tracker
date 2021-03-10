import paho.mqtt.client as mqtt
import meraki


#Callback for client connection (CONNACK received)
def on_connect(client, userData, flags, rc):
    print("Connected with result code: " + str(rc))
    
    client.subscribe("/merakimv/Q2EV-TWQP-G8VX/raw_detections")


#Callback for client receiving a publish message from server
def on_message(client, userData, msg):
    if len(eval(msg.payload)['objects']) > 2:
        print(msg.payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()
