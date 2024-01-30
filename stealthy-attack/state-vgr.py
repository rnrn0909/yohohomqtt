from paho.mqtt import client as mqtt_client
import random
import logging
import time
import json
from datetime import datetime

# address
# 192.168.0.10 : Main controller SSC
# 192.168.0.11 : MPO
# 192.168.0.12 : HBW
# 192.168.0.13 : VGR
# 192.168.0.14 : SLD

client_id = f'ft-txt-{random.randint(0, 10000)}'
username = 'txt'
password = 'xtx'
BROKER = '192.168.0.10'
PORT = 1883
FLAG_EXIT = False
PUB_TOPIC = 'f/i/state/vgr'
SUB_TOPIC = 'f/#'      

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker!")
            client.subscribe(SUB_TOPIC)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    try:
        client.connect(BROKER, PORT)
    except Exception as err:
        print(err)
        global FLAG_EXIT
        FLAG_EXIT= True
    return client

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)
        try:
            client.reconnect()
            logging.info("Reconnected Successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)
        
        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count +=1 

    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    global FLAG_EXIT
    FLAG_EXIT = True

def publish(client):
    msg_count = 0
    while not FLAG_EXIT:
        now = datetime.now()
        current_ts = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        cts = str(current_ts) + 'Z'
        msg_dict = { 
            "active" : 0,
            "code" : 1,
            "description" : "",
            "station" : "vgr",
            "target" : "",
            'ts': cts             
             }
        msg = json.dumps(msg_dict)
        if not client.is_connected():
            logging.error(" P U B L I S H : MQTT client is not connected!")
            time.sleep(1)
            continue
        result = client.publish(PUB_TOPIC, msg, 2)
        status = result[0]
        if status == 0:
            print(f'Send `{msg}` to topic `{PUB_TOPIC}`')
        else:
            print(f'Failed to send message to topic {PUB_TOPIC}')
        msg_count += 1
        time.sleep(0.4)

def subscribe(client):
    def on_message(client, userdata, msg):
        print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')
    client.subscribe(SUB_TOPIC)
    client.on_message = on_message

def run():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
    client = connect_mqtt()
    client.loop_start()
    time.sleep(1)
    if client.is_connected():
        publish(client)
    else:
        client.loop_stop()



if __name__=='__main__':
    try:
        if FLAG_EXIT == True:
            print("\nDisconnected. ")
            exit
        else:
            run()
    except KeyboardInterrupt as e:
        print("\nInterrupted. ")
        exit 
