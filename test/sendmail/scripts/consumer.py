import pika
# from mailer import send_html_mail, send_mail
from django.core.mail import send_mail
import json
from django.conf import settings
import os

settings.configure()


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='message')


def callback(ch, method, properties, body):
    bodys = json.loads(body)
    print('[x] Received ', bodys)
    send_mail('kkkkk', 'gfhgfhh', 'deepython@yandex.ru', ['avtogranica@yandex.ru'])
    # send_html_mail(subject=bodys['subject'],
    #                message=bodys['message_plaintext'],
    #                from_email=bodys['from_email'],
    #                recipient_list=bodys['recipients'],
    #                message_html=bodys['message_html'])
    # print(' [x] Received {0}\n by {1}\n with properties {2}\n via {3}\n'.format(
    #     body,
    #     method,
    #     properties,
    #     ch,
    # ))


channel.basic_consume(
    queue='message',
    auto_ack=True,
    on_message_callback=callback,
)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
