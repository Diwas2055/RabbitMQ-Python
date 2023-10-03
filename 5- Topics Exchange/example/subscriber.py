import pika
import sys
from config import settings


class Subscriber:
    def __init__(self, queueName, bindingKey, config, credentials):
        self.queueName = queueName
        self.bindingKey = bindingKey
        self.config = config
        self.credentials = credentials
        self.connection = self._create_connection()

    def __del__(self):
        self.connection.close()

    def _create_connection(self):
        credentials = pika.PlainCredentials(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        parameters = pika.ConnectionParameters(
            host=self.config["host"],
            port=self.config["port"],
            credentials=credentials,
            ssl_options=self.config["ssl"],
            virtual_host=self.config["vhost"],
            heartbeat=self.config["heartbeat"],
            blocked_connection_timeout=self.config["blocked_timeout"],
            retry_delay=self.config["retry_delay"],
        )
        return pika.BlockingConnection(parameters)

    def on_message_callback(self, channel, method, properties, body):
        print("body -", body)

    def setup(self):
        print("setup started")
        channel = self.connection.channel()

        # This method creates or checks a queue
        channel.queue_declare(queue=self.queueName)
        print("Queue declared")

        # Binds the queue to the specified exchange
        channel.queue_bind(
            queue=self.queueName,
            exchange=self.config["exchange"],
            routing_key=self.bindingKey,
        )

        channel.basic_consume(
            queue=self.queueName,
            on_message_callback=self.on_message_callback,
            auto_ack=True,
        )

        print(" [*] Waiting for data for " + self.queueName + ". To exit press CTRL+C")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()


credentials = {
    "username": settings.get("rabbitmq", "").get("user"),
    "password": settings.get("rabbitmq", "").get("password"),
}

config = {
    "host": settings.get("rabbitmq", "").get("host"),
    "port": settings.get("rabbitmq", " ").get("port"),
    "vhost": settings.get("rabbitmq", " ").get("vhost"),
    "ssl": settings.get("rabbitmq", " ").get("ssl"),
    "heartbeat": settings.get("rabbitmq", " ").get("heartbeat"),
    "blocked_timeout": settings.get("rabbitmq", " ").get("blocked_timeout"),
    "retry_delay": settings.get("rabbitmq", " ").get("retry_delay"),
    "exchange": "my_exchange",
}

if len(sys.argv) < 2:
    print("Usage: " + __file__ + " <QueueName> <BindingKey>")
    sys.exit()
else:
    queueName = sys.argv[1]
    # key in the form exchange.*
    key = sys.argv[2]
    subscriber = Subscriber(queueName, key, config, credentials)
    subscriber.setup()


# python subscriber.py testQueue black.#
