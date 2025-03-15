from app.config.db import db
from app.models.ingrediente import Ingrediente


class Base(Ingrediente):
    __tablename__ = 'bases'
    
    id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
    sabor = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'base',
        'inherit_condition': (id == Ingrediente.id)
    }