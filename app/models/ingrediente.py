from app.config.db import db


class TipoIngrediente(db.Model):
    __tablename__ = 'tipo_ingrediente'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    ingredientes = db.relationship('Ingrediente', back_populates='tipo_ingrediente')

class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Float, nullable=False)
    es_vegetariano = db.Column(db.Boolean, default=True)
    # Este campo era antiguo y se remplazó por tipo_ingrediente, para traer los ingredientes directamente desde otra tabla
    # tipo = db.Column(db.String(50), nullable=False)
    tipo_ingrediente_id = db.Column(db.Integer, db.ForeignKey('tipo_ingrediente.id'), nullable=False)
    tipo_ingrediente = db.relationship('TipoIngrediente', back_populates='ingredientes')
    productos = db.relationship('ProductoIngrediente', back_populates='ingrediente')

    def __repr__(self):
        return f"<Ingrediente {self.nombre}>"