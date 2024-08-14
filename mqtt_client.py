
# backend/mqtt_client.py
import paho.mqtt.client as mqtt
from shared import subscriptions, socketio

MQTT_BROKER = 'localhost'  # Change to your MQTT broker address
MQTT_PORT = 1883            # Default MQTT port

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    if msg.topic in subscriptions:
        # Emit only if the topic is subscribed
        socketio.emit('new_message', {'topic': msg.topic, 'message': msg.payload.decode()})


client.on_connect = on_connect
client.on_message = on_message

def connect_mqtt():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

def publish_message(topic, message):
    client.publish(topic, message)

def subscribe_topic(topic):
    client.subscribe(topic)

def unsubscribe_topic(topic):
    client.unsubscribe(topic)
