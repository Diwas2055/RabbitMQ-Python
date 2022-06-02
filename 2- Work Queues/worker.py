#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# It declares a queue named task_queue. The durable option makes the queue survive a broker restart.
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    
    # It tells RabbitMQ that a particular message has been received, processed and that RabbitMQ is
    # free to delete it.
    ch.basic_ack(delivery_tag=method.delivery_tag)


# It tells RabbitMQ not to give more than one message to a worker at a time. Or, in other words, don't
# dispatch a new message to a worker until it has processed and acknowledged the previous one.
# Instead, it will dispatch it to the next worker that is not still busy.
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()