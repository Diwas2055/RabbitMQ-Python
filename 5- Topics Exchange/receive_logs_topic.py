#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

#! To receive all the logs run:
#    python receive_logs_topic.py "#"

#! To receive all logs from the facility "kern":
#    python receive_logs_topic.py "kern.*"

#! Or if you want to hear only about "critical" logs:
#    python receive_logs_topic.py "*.critical"

#!  You can create multiple bindings:
#    python receive_logs_topic.py "kern.*" "*.critical"

#! And to emit a log with a routing key "kern.critical" type:
#   python emit_log_topic.py "kern.critical" "A critical kernel error"