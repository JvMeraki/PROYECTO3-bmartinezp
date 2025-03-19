from flask import Flask
from flask_login import LoginManager

from app.config.config import Config
from app.config.db import db
from app.config.routes import register_routes
from app.controllers.auth import auth_bp
from app.controllers.ingredientes_controller import ingredientes_bp
from app.controllers.productos_controller import productos_bp
from app.controllers.ventas_controller import ventas_bp

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app(config_app=Config):
    app = Flask(__name__, template_folder="views", static_folder="static")
    
    app.config.from_object(config_app)
    db.init_app(app)
    login_manager.init_app(app)
    register_routes(app)  # Registra rutas generales

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(productos_bp, url_prefix="/productos") 
    app.register_blueprint(ventas_bp)
    app.register_blueprint(ingredientes_bp, url_prefix="/ingredientes")

    from app.models.heladeria import Heladeria
    from app.models.ingrediente import Ingrediente
    from app.models.producto import Producto
    from app.models.producto_ingrediente import ProductoIngrediente
    
    print("Tipos de ingredientes insertados correctamente.")
    with app.app_context():
        db.create_all()
        
        from app.models.ingrediente import TipoIngrediente

        # Se mandan quemados estos tipos de ingrediente a la BD para evitar tener que crearlos manualmente
        # Se pueden agregar más de ser necesario o eliminar si es necesario
        tipos_ingredientes = [
            'Fruta', 'Saborizante', 'Frutos Secos', 'Lácteo', 'Untable', 'Endulzante',
            'Especia', 'Hierba', 'Topping', 'Salsa', 'Helado', 'Dulce', 'Chocolate',
            'Verdura', 'Semilla'
        ]

        for tipo in tipos_ingredientes:
            if not TipoIngrediente.query.filter_by(nombre=tipo).first():
                db.session.add(TipoIngrediente(nombre=tipo))

        db.session.commit()
        print("Tipos de ingredientes insertados correctamente.")
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))