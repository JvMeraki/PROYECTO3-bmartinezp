from app.config.db import db
from app.models.producto import Producto


class Copa(Producto):
    __tablename__ = 'copas'
    id = db.Column(db.Integer, db.ForeignKey('producto.id'), primary_key=True)
    tipo_vaso = db.Column(db.String(50), nullable=False)
    
    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self.obtener_ingredientes())
    
    def calcular_calorias(self):
        return super().calcular_calorias() * 0.95

    __mapper_args__ = {
        'polymorphic_identity': 'Copa',
    }