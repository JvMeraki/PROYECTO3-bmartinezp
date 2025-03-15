from ingrediente import Ingrediente

from app.config.db import db


class Complemento(Ingrediente):
    __tablename__ = 'complementos'
    id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'complemento',
    }