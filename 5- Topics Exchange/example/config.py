from dotenv import dotenv_values


env_values = dotenv_values(".env")

settings = {
    "rabbitmq": {
        "host": env_values.get("RABBITMQ_HOST"),
        "port": env_values.get("RABBITMQ_PORT"),
        "user": env_values.get("RABBITMQ_USER"),
        "password": env_values.get("RABBITMQ_PASSWORD"),
        "vhost": env_values.get("RABBITMQ_VHOST", "/"),
        "ssl": env_values.get("RABBITMQ_SSL")
        if env_values.get("RABBITMQ_SSL")
        else None,
        "blocked_timeout": float(env_values.get("RABBITMQ_BLOCKED_CONNECTION_TIMEOUT")),
        "heartbeat": int(env_values.get("RABBITMQ_HEARTBEAT")),
        "retry_delay": int(env_values.get("RABBITMQ_RETRY_DELAY")),
    }
}
