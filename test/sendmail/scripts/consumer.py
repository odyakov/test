import pika
from django.core.mail import send_mail
import json
from django.conf import settings


settings.configure()

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='message')


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(' [x] Received ', data)
    send_mail(**data)


channel.basic_consume(
    queue='message',
    auto_ack=True,
    on_message_callback=callback,
)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
