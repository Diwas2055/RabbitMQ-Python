import pika

from config import settings


class Publisher:
    def __init__(self, config, credentials):
        self.config = config
        self.credentials = credentials

    def publish(self, routing_key, message):
        connection = self.create_connection()
        channel = connection.channel()

        """
        Creates/verifies an exchange.
        """
        channel.exchange_declare(
            exchange=self.config["exchange"], exchange_type="topic"
        )

        # Publish 'message' to the 'exchange' matching
        # the provided routing key
        channel.basic_publish(
            exchange=self.config["exchange"], routing_key=routing_key, body=message
        )

        print(f" [x] Sent message {message} for {routing_key}")

    # Create new connection
    def create_connection(self):
        credentials = pika.PlainCredentials(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        param = pika.ConnectionParameters(
            host=self.config["host"],
            port=self.config["port"],
            credentials=credentials,
            ssl_options=self.config["ssl"],
            virtual_host=self.config["vhost"],
            heartbeat=self.config["heartbeat"],
            blocked_connection_timeout=self.config["blocked_timeout"],
            retry_delay=self.config["retry_delay"],
        )
        return pika.BlockingConnection(param)


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
publisher = Publisher(config, credentials)
publisher.publish("black", "single word routing key")
publisher.publish("black.mamba", "one more word added")
publisher.publish("black.abc.xyz", "one or more words")
publisher.publish("white.abc.xyz", "This is a white message")


# python publisher.py
