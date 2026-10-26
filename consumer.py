#!/usr/bin/env python3
"""Consume and acknowledge one message; fail if no message arrives in 15 s."""
import os
import pika


def main():
    host = os.environ.get('RMQ_HOST', 'localhost')
    credentials = pika.PlainCredentials(os.environ.get('RMQ_USER', 'student'), os.environ['RMQ_PASSWORD'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))
    try:
        channel = connection.channel()
        channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'classic'})
        channel.basic_qos(prefetch_count=1)
        print(f'[*] Waiting for a message from hello via {host}', flush=True)
        for method, properties, body in channel.consume('hello', inactivity_timeout=15, auto_ack=False):
            if method is None:
                raise SystemExit('No message received within 15 seconds')
            print(f'[x] Received {body.decode()!r}', flush=True)
            channel.basic_ack(method.delivery_tag)
            channel.cancel()
            break
    finally:
        connection.close()


if __name__ == '__main__':
    main()
