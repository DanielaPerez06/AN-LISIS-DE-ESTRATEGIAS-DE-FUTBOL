from config import Document, IntField, StringField, ListField, DictField, EmbeddedDocument, EmbeddedDocumentField
#Clase lineups delimita los datos que voy a mandar a mongo
class Player(EmbeddedDocument):
    nombre = StringField(required=True)
    numero = IntField(required=True)
    posicion = StringField(required=True)
    grid = StringField(required=True)

class Lineups(Document):
    partidoid = IntField(required=True)
    equipo = StringField(required=True)
    formacion = StringField(required=True)
    titulares = ListField(EmbeddedDocumentField(Player))
    # titulares es una lista de datos (array) que contiene subdatos, por eso es un embedded document
    #facilita la vision de datos en mongo