#!/usr/bin/env python3
"""Send one confirmed, persistent message to the classic queue hello."""
import os
import pika


def main():
    host = os.environ.get('RMQ_HOST', 'localhost')
    credentials = pika.PlainCredentials(os.environ.get('RMQ_USER', 'student'), os.environ['RMQ_PASSWORD'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))
    try:
        channel = connection.channel()
        channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'classic'})
        channel.confirm_delivery()
        message = os.environ.get('RMQ_MESSAGE', 'Hello World!')
        channel.basic_publish(exchange='', routing_key='hello', body=message.encode(),
                              properties=pika.BasicProperties(delivery_mode=2), mandatory=True)
        print(f"[x] Sent {message!r} to hello via {host}", flush=True)
    finally:
        connection.close()


if __name__ == '__main__':
    main()
