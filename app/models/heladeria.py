from app.config.db import db


class Heladeria(db.Model):
    __tablename__ = 'heladeria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    ventas = db.Column(db.Float, default=0, nullable=False)
    productos = db.relationship('Producto', backref='heladeria', lazy=True)

    def __repr__(self):
        return f"<Heladeria {self.nombre}>"