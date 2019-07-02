import paho.mqtt.client as mqtt
from random import randint
from datetime import datetime

BROKER = 'raspberrypi.local'
TOPIC_HEAD = 'RollE_MKII/'


def defineClient(client_id):
    client = mqtt.Client(client_id)
    return client

def connected(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def publisher_init(client):
    #instantiates mqtt client connects to broker and awaits messages in endless loop
    client.on_connect = connected
    client.connect(BROKER)
    print('setting up done, starting ...')

def subscriber_init(client):
    #instantiates mqtt client connects to broker and awaits messages in endless loop
    client.on_connect = connected
    client.on_message = message_in
    client.connect(BROKER)

    print('setting up done, starting ...')
    client.loop_forever()


def message_in(client,userdata,msg):
    print("Time: " + datetime.now().strftime('%Y-%m-%d %H.%M.%S.%f') + "    Topic: "+msg.topic+"        Message: "+str(msg.payload))
    return(msg.topic,msg.payload)
        
def publish_value(client, msg,topic):
    client.publish( TOPIC_HEAD+topic, msg)
    client.loop()

def subscribe(client,topic):
    client.subscribe(topic)


