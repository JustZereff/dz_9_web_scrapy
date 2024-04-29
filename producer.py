# Подключаем необходимые модули

import os
from mongoengine import connect
import pika
from models import Quotes, Author
import json


# Шлях до файлу
current_directory = os.path.dirname(__file__)
quotes_file = os.path.join(current_directory, 'myspider', 'quotes.json')
authors_file = os.path.join(current_directory, 'myspider', 'authors.json')

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
channel.queue_declare(queue='author_id')

# Додаємо цитати до бази данних, та відправляємо до RebbitMQ
def generate_quotes():
    with open(authors_file, 'r', encoding='UTF-8') as fn:
        authors_json_file = json.load(fn)
    
    with open(quotes_file, 'r', encoding='UTF-8') as fn:
        quotes_json_file = json.load(fn)
    
    for author_dict in authors_json_file:
        author = Author(
                fullname=author_dict.get('fullname'),
                born_date=author_dict.get('born_date'),
                born_location=author_dict.get('born_location'),
                description=author_dict.get('description'),
                message_sent = False
            )
        author.save()
        # Відправляємо повідомлення с ObjectID в очередь RabbitMQ
        message = {'author_id': str(author.id)}  # Преобразуем ObjectID в строку для JSON
        channel.basic_publish(exchange='', routing_key='author_id', body=json.dumps(message))

    for quote_dict in quotes_json_file:
        author_name = quote_dict.get('author')
        author = Author.objects(fullname=author_name).first()
        if author:
            quote = Quotes(
                quote = quote_dict.get('quote'),
                author = quote_dict.get('author'),
                tags = quote_dict.get('tags')
            )
        quote.save()
        
        
    print('Автори створені та відправлені до RebbitMQ')

if __name__ == "__main__":
    
    generate_quotes()
