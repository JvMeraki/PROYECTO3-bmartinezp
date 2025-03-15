from app.config.db import db
from app.models.producto import Producto


class Malteada(Producto):
    __tablename__ = 'malteada'
    id = db.Column(db.Integer, db.ForeignKey('producto.id'), primary_key=True)
    volumen = db.Column(db.Float, nullable=False)

    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self.obtener_ingredientes()) + 500
    
    def calcular_calorias(self):
        return super().calcular_calorias() + 200

    __mapper_args__ = {
        'polymorphic_identity': 'Malteada'
    }