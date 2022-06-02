#!/usr/bin/env python
import pika
import sys

# Creating a new instance of the `PlainCredentials` object.
credentials = pika.PlainCredentials('user', 'password')

#Create a new instance of the Connection object
connection= pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials= credentials))

channel = connection.channel()

# durable=True ( It makes sure that RabbitMQ will never lose our queue.) 
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
print(" [x] Sent %r" % message)
connection.close()

    #? Command to run:
# python new_task.py First message.
# python new_task.py Second message..
# python new_task.py Third message...
# python new_task.py Fourth message....
# python new_task.py Fifth message.....