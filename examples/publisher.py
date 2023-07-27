from sensors.publisher import get_client


def main():
    with get_client() as client:
        for index in range(10):
            client.publish("sensors/temperature", payload=index)


if __name__ == "__main__":
    main()
