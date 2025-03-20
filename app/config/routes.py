from functools import wraps

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, send_from_directory, url_for)
from flask_login import current_user, login_required

from app.config.auth_decorator import role_required
from app.config.db import db
from app.models.ingrediente import Ingrediente
from app.models.producto import Producto

auth_bp = Blueprint('api', __name__)

def register_routes(app):
    app.register_blueprint(auth_bp)
    
    @app.route("/no_autorizado")
    def no_autorizado():
        return render_template("no_autorizado.html"), 403

    @app.route("/")
    def home():
        productos = Producto.query.all()
        return render_template("index.html", productos=productos)

    @app.route("/api")
    @role_required("is_admin", "is_employee", "is_client")
    def api():
        productos = Producto.query.all()
        for producto in productos:
            print(f"Producto en Flask: ID={producto.id}, Nombre={producto.nombre}")
        return render_template("api.html", productos=productos)
    
    @app.route("/documentacion")
    def documentacion():
        productos = Producto.query.all()
        return render_template("api_doc.html", productos=productos)
    
    @app.route('/productos_json', methods=['GET'])
    def obtener_productos():
        productos = Producto.query.all()
        return jsonify([producto.to_dict() for producto in productos])

    @app.route('/producto/<int:producto_id>', methods=['GET'])
    def obtener_producto(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            return jsonify(producto.to_dict())
        return jsonify({"error": "Producto no encontrado"}), 404
    
    @app.route('/productos/editar/<int:producto_id>', methods=['GET', 'POST'])
    @role_required("is_admin", "is_employee")
    def editar_producto(producto_id):
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

    @app.route('/producto/nombre/<string:nombre>', methods=['GET'])
    def obtener_producto_por_nombre(nombre):
        producto = Producto.query.filter_by(nombre=nombre).first()
        if producto:
            return jsonify(producto.to_dict())
        return jsonify({"error": "Producto no encontrado"}), 404

    @app.route('/producto/<int:producto_id>/calorias', methods=['GET'])
    @role_required("is_admin", "is_employee", "is_client")
    def consultar_calorias(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            return jsonify({"calorias": producto.calcular_calorias()})
        return jsonify({"error": "Producto no encontrado"}), 404

    @app.route('/producto/<int:producto_id>/rentabilidad', methods=['GET'])
    @role_required("is_admin")
    def consultar_rentabilidad(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            return jsonify({"rentabilidad": producto.calcular_rentabilidad()})
        return jsonify({"error": "Producto no encontrado"}), 404

    @app.route('/producto/<int:producto_id>/costo', methods=['GET'])
    @role_required("is_admin", "is_employee")
    def consultar_costo(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            return jsonify({"costo_produccion": producto.calcular_costo()})
        return jsonify({"error": "Producto no encontrado"}), 404

    @app.route('/producto/<int:producto_id>/vender', methods=['POST'])
    @role_required("is_admin", "is_employee", "is_client")
    def vender_producto(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            producto.vender()
            db.session.commit()
            return jsonify({"mensaje": "Producto vendido con éxito"})
        return jsonify({"error": "Producto no encontrado"}), 404

    @app.route('/ingredientes_json', methods=['GET'])
    def obtener_ingredientes():
        ingredientes = Ingrediente.query.all()
        return jsonify([ingrediente.to_dict() for ingrediente in ingredientes])

    @app.route('/ingrediente/<int:ingrediente_id>', methods=['GET'])
    def obtener_ingrediente(ingrediente_id):
        ingrediente = Ingrediente.query.get(ingrediente_id)
        if ingrediente:
            return jsonify(ingrediente.to_dict())
        return jsonify({"error": "Ingrediente no encontrado"}), 404

    @app.route('/ingrediente/nombre/<string:nombre>', methods=['GET'])
    def obtener_ingrediente_por_nombre(nombre):
        ingrediente = Ingrediente.query.filter_by(nombre=nombre).first()
        if ingrediente:
            return jsonify(ingrediente.to_dict())
        return jsonify({"error": "Ingrediente no encontrado"}), 404

    @app.route('/ingrediente/<int:ingrediente_id>/saludable', methods=['GET'])
    def verificar_saludable(ingrediente_id):
        ingrediente = Ingrediente.query.get(ingrediente_id)
        if ingrediente:
            return jsonify({"saludable": ingrediente.es_saludable()})
        return jsonify({"error": "Ingrediente no encontrado"}), 404

    @app.route('/producto/<int:producto_id>/reabastecer', methods=['POST'])
    @role_required("is_admin", "is_employee")
    def reabastecer_producto(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            producto.reabastecer()
            db.session.commit()
            return jsonify({"mensaje": "Producto reabastecido con éxito"})
        return jsonify({"error": "Producto no encontrado"}), 404

    @app.route('/producto/<int:producto_id>/renovar', methods=['POST'])
    @role_required("is_admin", "is_employee")
    def renovar_inventario(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            producto.renovar_inventario()
            db.session.commit()
            return jsonify({"mensaje": "Inventario renovado con éxito"})
        return jsonify({"error": "Producto no encontrado"}), 404
