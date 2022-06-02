#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()


#! If you want to save only 'warning' and 'error' (and not 'info') log messages to a file, just open a console and type:

# python receive_logs_direct.py warning error > logs_from_rabbit.log

#! If you'd like to see all the log messages on your screen, open a new terminal and do:

# python receive_logs_direct.py info warning error

#! And, for example, to emit an error log message just type:

# python emit_log_direct.py error "Run. Run. Or it will explode."