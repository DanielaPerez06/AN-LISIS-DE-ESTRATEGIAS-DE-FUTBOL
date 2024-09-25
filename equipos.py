from config import Document, IntField, DateTimeField, StringField, DictField, URLField

class Equipos(Document):
    equipoid = IntField(required=True)
    nombre = StringField(required=True)
    logo = URLField(required=True)