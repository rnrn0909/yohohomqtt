import time
import logging
import random
from paho.mqtt import client as mqtt_client
import json


# reference: https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-Python3/sub_tcp.py 

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
TOPIC = '#'

def connect_mqtt():
    def on_message(client, userdata, msg):
                print(f'Received `{msg.payload.decode()}` | `{msg.qos}` | `{msg.topic}`')
                payload = json.loads(msg.payload.decode())
                timestamp = payload["ts"]
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info(f'{client_id}: Connected flags {flags} | {rc}')
            print('Connected to MQTT broker!')
            client.connected_flag = True
            client.subscribe(TOPIC)
            client.on_message = on_message

        else:
            print("Failed to connect, return code %d\n", rc)
    # client = mqtt_client.Client(client_id)
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect

    try:
        client.connect(BROKER, PORT, keepalive=120)
        client.on_disconnect = on_disconnect
    except Exception as err:
        print('Error: ', err)
        global FLAG_EXIT
        # conn.close()
        FLAG_EXIT = True
    return client

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECOONECT_COUNT = 12
MAX_RECONNECT_DELAY = 60


def on_disconnect(client, userdata, rc):
    logging.info('Disconnected with result code: %s', rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECOONECT_COUNT:
        logging.info('Reconnecting in %d seconds...', reconnect_delay)
        time.sleep(reconnect_delay)
        try:
            client.reconnect()
            logging.info('Reconnected Successfully!')
            return
        except Exception as err:
            logging.error('%s. Reconnect failed. Retrying...', err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay  = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1

    logging.info('Reconnect failed after %s attempts. Exiting... ', reconnect_count)
    global FLAG_EXIT
    FLAG_EXIT = True

def run():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
    client = connect_mqtt()
    client.loop_forever()


if __name__ == '__main__':
    try:
        if FLAG_EXIT == True:
            print("\nDisconnected. ")
            exit
        else:
            run()
    except KeyboardInterrupt as e:
        print('\nInterrupted. ')
        exit
