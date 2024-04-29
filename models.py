""" Створення моделей. """

from mongoengine import Document, StringField, ListField, BooleanField, ReferenceField

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    message_sent = BooleanField(default=False)

class Quotes(Document):
    quote = StringField()
    author = ReferenceField(Author, reverse_delete_rule='CASCADE')
    tags = ListField(StringField())
