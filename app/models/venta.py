from datetime import datetime

from app.config.db import db


class Venta(db.Model):
    __tablename__ = 'venta'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now)
    total = db.Column(db.Float, nullable=False, default=0)

    # Relación con DetalleVenta (cada venta puede tener múltiples productos)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)

    def calcular_total(self):
        return sum(detalle.total for detalle in self.detalles)