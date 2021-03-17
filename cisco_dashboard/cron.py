import meraki
import django
import time
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cisco_dashboard.settings')
django.setup()

from main.models import Snapshot
from main.models import Device
from main.models import Network
from datetime import datetime

import paho.mqtt.client as mqtt


key    = "4f9d726866f2cb8da55221caf1f46ba34293449c"
serial = "Q2EV-TWQP-G8VX"

dash = meraki.DashboardAPI(key)


def on_connect(client, userData, flags, rc):
    """
    * Callback function for client connection
    * Means a CONNACK was received
    """
    client.subscribe("/merakimv/Q2EV-TWQP-G8VX/raw_detections")


def on_message(client, userData, msg):
    """
    * Callback function
    * Means client received publish message from MQTT broker
    """
    if len(eval(msg.payload)['objects']) > 1:
        timestamp = datetime.fromtimestamp(time.time()).isoformat()
        response = dash.camera.generateDeviceCameraSnapshot(serial, ts = timestamp)

        snapDevice = None

        try:
            snapDevice = Device.objects.filter(devSerial = serial)[0]

        except:
            print("Device not found")

        new_snapshot = Snapshot.objects.create(
            net = snapDevice.net.org,
            url = response['url'],
            time = string(timestamp)
        )
        new_snapshot.save()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()
