from .publisher import get_client
from .sensor import get_dht_device, meausure


def main():
    with get_client() as client:
        with get_dht_device() as dht_device:
            for data in meausure(dht_device):
                client.publish(
                    "sensors/temperature",
                    payload=data.serialize(),
                )


main()
