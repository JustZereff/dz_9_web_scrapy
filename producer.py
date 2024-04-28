# Подключаем необходимые модули

import os
from mongoengine import connect
import pika
from models import Quotes
import json


# Шлях до файлу
current_directory = os.path.dirname(__file__)
quotes_file = os.path.join(current_directory, 'myspider', 'quotes.json')

# Открываем файлы с паролями
with open('password.txt', 'r') as file_pass:
    password = file_pass.read()
    
with open('password_from_CloudAMQP.txt', 'r') as file_pass_cloudamqp:
    password_from_CloudAMQP = file_pass_cloudamqp.read()

# Формируем URL для подключения к MongoDB и RabbitMQ
URL = f'mongodb+srv://tapxyh1445:{password}@nosqlbase.zekqidk.mongodb.net/'
URL_FOR_CLOUDAMQP = f'amqps://fbvnpspi:{password_from_CloudAMQP}@sparrow.rmq.cloudamqp.com/fbvnpspi'

# Подключаемся к MongoDB
connect(host=URL)

# Подключаемся к RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(URL_FOR_CLOUDAMQP))
channel = connection.channel()
channel.queue_declare(queue='contact_id')

# Додаємо цитати до бази данних, та відправляємо до RebbitMQ
def generate_quotes():
    with open(quotes_file, 'r', encoding='UTF-8') as fn:
        quotes_json_file = json.load(fn)
        
    for quote_dict in quotes_json_file:
        quote = Quotes(
                    quote = quote_dict.get('quote'),
                    author = quote_dict.get('author'),
                    tags = quote_dict.get('tags'),
                    message_sent = False
                )
        quote.save()
        
        # Відправляємо повідомлення с ObjectID в очередь RabbitMQ
        message = {'quotes_id': str(quote.id)}  # Преобразуем ObjectID в строку для JSON
        channel.basic_publish(exchange='', routing_key='quotes_id', body=json.dumps(message))
    print('Контакти створені та відправлені до RebbitMQ')

if __name__ == "__main__":
    
    generate_quotes()
