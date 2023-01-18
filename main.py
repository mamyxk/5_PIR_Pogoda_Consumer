import json
import pika


def rabbit_callback(ch, method, properties, body):
    try:
        recv = json.loads(body)
        print(f"Received message: {recv}")
    except json.decoder.JSONDecodeError as err:
        print(f"An error occured: {err}")

if __name__ == '__main__':
    try:
        config = None
        with open('app.conf.json') as json_file:
            config = json.load(json_file)
        print(config)

        rabbit_credentials = pika.PlainCredentials(
            config['rabbit']['login'],
            config['rabbit']['pass']
        )

        rabbit_params = pika.ConnectionParameters(
            config['rabbit']['host'],
            config['rabbit']['port'],
            config['rabbit']['vhost'],
            rabbit_credentials
        )
        rabbit_connection = pika.BlockingConnection(rabbit_params)
        channel = rabbit_connection.channel()
        channel.queue_declare(queue='pogoda')
        channel.basic_consume(queue='pogoda',
                        auto_ack=True,
                        on_message_callback=rabbit_callback)
        channel.start_consuming()
    except KeyboardInterrupt as err:
        print(f"Interrupted {err}")
        print("Stopping")
