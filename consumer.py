import pika
import json
from models import Author
from producer import URL_FOR_CLOUDAMQP

# Подключаемся к RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(URL_FOR_CLOUDAMQP))
channel = connection.channel()
channel.queue_declare(queue='author_id')

def callback(ch, method, properties, body):
    message = json.loads(body)
    author_id = message.get('author_id')
    
    author = Author.objects(id=author_id).first()
    if author:
        author.message_sent = True
        author.save()
        print(f'message_sent змінено на True у {author.fullname}')
    else:
        print('Авторів не знайдено.')

channel.basic_consume(queue='author_id', on_message_callback=callback, auto_ack=True)

channel.start_consuming()