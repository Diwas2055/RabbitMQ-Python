#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
    """
    "If n is 0, return 0. If n is 1, return 1. Otherwise, return the sum of the previous two fibonacci
    numbers."
    
    The first two lines of the function are called the base case. They are the simplest possible cases
    that we can solve. The third line is called the recursive case. It is the case where we have to make
    a recursive call to solve the problem
    
    :param n: the number of the Fibonacci number you want to find
    :return: The nth number in the Fibonacci sequence.
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    # Calling the fib function with the value of n.
    response = fib(n)

    # Publishing the response to the queue that the client is listening to.
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    
    # Acknowledging that the message has been received and processed.
    ch.basic_ack(delivery_tag=method.delivery_tag)

# It tells RabbitMQ not to give more than one message to a worker at a time. Or, in other words,
# don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
# Instead, it will dispatch it to the next worker that is not still busy.
channel.basic_qos(prefetch_count=1)
# Telling RabbitMQ to call the on_request function whenever a message is received.
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()