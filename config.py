from mongoengine import connect, Document, IntField, DateTimeField, StringField, DictField, ListField, EmbeddedDocument, EmbeddedDocumentField, URLField

# Conectar a la base de datos 'futbol'
connect(db='futbol', host='localhost', port=27017)

# Definir un documento (una colección en MongoDB)
class Jugador(Document):
    nombre = StringField(required=True)
    edad = IntField(required=True)

# Crear un nuevo jugador
nuevo_jugador = Jugador(nombre='Lionel Messi', edad=36)
nuevo_jugador.save()  # Esto guardará el documento en la base de datos

# Si este comando funciona, se habrá creado la base de datos y la colección 'jugador'
#print("Jugador guardado exitosamente.")


