import paho.mqtt.client as mqtt
import json
from codec import Codec
from dotenv import load_dotenv
import os 

codec = Codec()

load_dotenv()
user = os.environ.get('USER')
password = os.environ.get('PWD')
appname = os.environ.get('APP_NAME')
device = os.environ.get('DEVEUI')
host = os.environ.get('TTN_ADDR')

def on_publish(client, userdata, mid):
    print("Message Published...")

client = mqtt.Client()
client.on_publish = on_publish
client.username_pw_set(user, password=password)
client.connect("hanhomettn.iptime.org", 1883, 60)

message = codec.encode("Hello World!")

payload = {
    "downlinks": [
        {
            "f_port": 2,
            "frm_payload": message,
        }
    ]
}

client.publish(f"v3/{appname}/devices/{device}/down/push", json.dumps(payload))
client.disconnect()