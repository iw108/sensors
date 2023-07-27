
from paho.mqtt.client import Client, MQTTMessage


def on_connect(client: Client, userdata, flags, rc):
    client.subscribe("sensors/temperature")


def on_message(client, userdata, msg: MQTTMessage):
    print(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("127.0.0.1", 1883, 60)

    client.loop_forever()
