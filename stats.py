from mongoengine import Document, IntField, StringField, DictField
from config import connect  # Esto sigue siendo correcto si config maneja la conexión

class Stats(Document):
    partidoid = IntField(required=True)
    equipo = StringField(required=True)
    estadisticas = DictField(required=True)
