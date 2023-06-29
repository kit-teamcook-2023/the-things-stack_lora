import paho.mqtt.client as mqtt
import json
from codec import Codec
from dotenv import load_dotenv
import os 

codec = Codec()

load_dotenv()
user = os.environ.get('USER')
password = os.environ.get('PWD')
host=os.environ.get('TTN_ADDR')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    try:
        dict_string = msg.payload
        diction = json.loads(dict_string)
        print('topic:', msg.topic, ', time:', diction['received_at'])
        data = codec.decode(diction['uplink_message']['frm_payload'])
        print('message:', data)
    except:
        print("No connection")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=user, password=password)
client.connect(host, 1883, 60)

client.loop_forever()