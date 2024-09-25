from config import Document, IntField, DateTimeField, StringField, DictField  # Importa la clase desde config
#Clase partido, esto delimita los datos que voy a exportar a mongoDB
class Partido(Document):
    partidoid = IntField(required=True)
    fecha = DateTimeField(required=True)
    estado_partido = StringField(required=True)
    equipos = DictField(required=True)
    goles = DictField(required=True)
    
