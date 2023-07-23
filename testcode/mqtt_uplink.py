import paho.mqtt.client as mqtt
import json
# from codec import Codec
from dotenv import load_dotenv
import os 
import requests
from datetime import *

# codec = Codec()

load_dotenv()
user = os.environ.get('USER')
password = os.environ.get('PWD')
host=os.environ.get('TTN_ADDR')
APP_KEY = os.environ.get('APP_KEY')
URL = 'https://dapi.kakao.com/v2/local/geo/coord2address.json'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    try:
        dict_string = msg.payload
        diction = json.loads(dict_string)
        print('topic:', msg.topic, ', time:', diction['received_at'])
        data = diction['uplink_message']['decoded_payload']

        if data['lat'] != '-300.000000000000000':
            data = json_request(url=f"{URL}?y={data['lat']}&x={data['lng']}")
            print(data['documents'][0]['address']['address_name'])
    except:
        print("No connection")

def json_request(url='', encoding='utf-8'):
    headers = {'Authorization': 'KakaoAK {}'.format(APP_KEY)}
    resp = requests.get(url, headers=headers)
    return json.loads(resp.text)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=user, password=password)
client.connect(host, 1883, 60)

client.loop_forever()

# https://cruddbdbdeep.github.io/python/2018/11/02/reverse-geocoding.html