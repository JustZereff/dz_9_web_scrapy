""" Створення моделей. """

from mongoengine import Document, StringField, ListField, BooleanField

    
class Quotes(Document):
    quote = StringField()
    author = StringField()
    tags = ListField(StringField())
    message_sent = BooleanField(default=False)