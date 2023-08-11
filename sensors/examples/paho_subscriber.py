"""Script for subscribing to MQTT topic."""

from config import Settings
from paho.mqtt.client import Client, MQTTMessage


def _on_connect(client: Client, userdata, flags, rc: int):
    if rc == 0:
        client.subscribe("sensors/temperature")


def _on_message(client: Client, userdata, msg: MQTTMessage):
    print(f"{msg.topic}: {msg.payload!r}")


def main(*, _settings: Settings | None = None):
    settings = _settings or Settings()

    client = Client()
    client.on_connect = _on_connect
    client.on_message = _on_message

    client.connect(settings.MQTT_HOST, settings.MQTT_PORT)

    client.loop_forever()


if __name__ == "__main__":
    main()
