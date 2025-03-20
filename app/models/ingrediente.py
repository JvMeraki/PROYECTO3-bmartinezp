from app.config.db import db


class TipoIngrediente(db.Model):
    __tablename__ = 'tipo_ingrediente'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    ingredientes = db.relationship('Ingrediente', back_populates='tipo_ingrediente', cascade="all, delete")

    def __repr__(self):
        return f"<TipoIngrediente {self.nombre}>"

    def __str__(self):
        return self.nombre


class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Float, nullable=False)
    es_vegetariano = db.Column(db.Boolean, default=True)

    tipo_ingrediente_id = db.Column(db.Integer, db.ForeignKey('tipo_ingrediente.id', ondelete="CASCADE"), nullable=False)
    tipo_ingrediente = db.relationship('TipoIngrediente', back_populates='ingredientes')

    productos = db.relationship('ProductoIngrediente', back_populates='ingrediente', cascade="all, delete")
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "calorias": self.calorias,
            "inventario": self.inventario,
            "es_vegetariano": self.es_vegetariano
        }


    def __repr__(self):
        return f"<Ingrediente {self.nombre}, {self.tipo_ingrediente.nombre}>"

    def __str__(self):
        return f"{self.nombre} - {self.tipo_ingrediente.nombre}"