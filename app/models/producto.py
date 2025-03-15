from app.config.db import db


class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    costo_produccion = db.Column(db.Float, nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Discriminator column - Copa o Malteada
    heladeria_id = db.Column(db.Integer, db.ForeignKey('heladeria.id'), nullable=True)
    ingredientes = db.relationship('ProductoIngrediente', back_populates='producto')
    
    
    def obtener_ingredientes(self):
        return [pi.ingrediente for pi in self.ingredientes]

    def calcular_calorias(self):
        return sum(ingrediente.calorias for ingrediente in self.obtener_ingredientes())
    
    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self.obtener_ingredientes())
    
    def calcular_rentabilidad(self):
        return self.precio_publico - self.calcular_costo()
    
    def __repr__(self):
        return f"<Producto {self.nombre}>"
    
    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'producto'
    }