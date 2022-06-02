#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# It's creating a new exchange if it doesn't already exist.
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# It's creating a new queue, and the empty string as the queue name means that we're letting 
# the server choose a random queue name for us.
result = channel.queue_declare(queue='', exclusive=True)

# It's creating a new queue, and the empty string as the queue name means that we're
# letting the server choose a random queue name for us.
queue_name =result.method.queue

# It's binding the queue to the exchange.
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

# auto_ack=True ( It's telling RabbitMQ not to expect a reply from the consumer. ) 
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()


#! If you want to save logs to a file, just open a console and type:

# python receive_logs.py > logs_from_rabbit.log

#! If you wish to see the logs on your screen, spawn a new terminal and run:

# python receive_logs.py