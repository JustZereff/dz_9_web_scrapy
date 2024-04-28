import pika
import json
from models import Quotes
from producer import URL_FOR_CLOUDAMQP

# Подключаемся к RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(URL_FOR_CLOUDAMQP))
channel = connection.channel()
channel.queue_declare(queue='quotes_id')

def callback(ch, method, properties, body):
    message = json.loads(body)
    quotes_id = message.get('quotes_id')
    
    quote = Quotes.objects(id=quotes_id).first()
    if quote:
        quote.message_sent = True
        quote.save()
        print(f'message_sent змінено на True у {quote.author}')
    else:
        print('Авторів не знайдено.')

channel.basic_consume(queue='quotes_id', on_message_callback=callback, auto_ack=True)

channel.start_consuming()