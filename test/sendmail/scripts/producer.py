import pika
import json


def mail_to_queue(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='message')
    channel.basic_publish(
        exchange='',
        routing_key='message',
        body=json.dumps(msg),
    )
    print(" [x] Sent ", msg)
    connection.close()
