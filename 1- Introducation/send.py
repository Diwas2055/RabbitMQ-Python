#!/usr/bin/env python

#! Producer
import pika

# Creating a new instance of the `PlainCredentials` object.
credentials = pika.PlainCredentials('user', 'password')

#Create a new instance of the Connection object
connection= pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials= credentials))

#Create a new channel with the next available channel number or pass in a channel number to use
channel = connection.channel()

#Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World! This is my First Message')    

print("[x] Sent 'Hello World!'")

connection.close()