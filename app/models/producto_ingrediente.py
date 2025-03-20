from app.config.db import db


class ProductoIngrediente(db.Model):
    __tablename__ = 'producto_ingrediente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)

    producto = db.relationship('Producto', back_populates='ingredientes')
    ingrediente = db.relationship('Ingrediente', back_populates='productos')
    
    def to_dict(self):
        return {
            "id": self.id,
            "ingrediente": {
                "id": self.ingrediente.id,
                "nombre": self.ingrediente.nombre,
                "precio": self.ingrediente.precio,
                "calorias": self.ingrediente.calorias
            }
        }