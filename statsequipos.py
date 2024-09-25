from config import Document, IntField, StringField, DictField, EmbeddedDocument, EmbeddedDocumentField

class PartidosStat(EmbeddedDocument):
    total = IntField(required=True)
    home = IntField(required=True)
    away = IntField(required=True)

class GolesStat(EmbeddedDocument):
    total = IntField(required=True)
    home = IntField(required=True)
    away = IntField(required=True)

class EstadisticasEquipo(Document):
    equipoid = IntField(required=True)
    nombre = StringField(required=True)
    partidos_jugados = EmbeddedDocumentField(PartidosStat)
    partidos_ganados = EmbeddedDocumentField(PartidosStat)
    empates = EmbeddedDocumentField(PartidosStat)
    partidos_perdidos = EmbeddedDocumentField(PartidosStat)
    goles_totales = EmbeddedDocumentField(GolesStat)


