from app.config.db import db


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'

    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

    producto = db.relationship('Producto')