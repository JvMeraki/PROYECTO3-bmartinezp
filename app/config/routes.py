from flask import (Blueprint, jsonify, render_template, request,
                   send_from_directory)

from app.config.db import db
from app.models.ingrediente import Ingrediente
from app.models.producto import Producto

auth_bp = Blueprint('api', __name__)

def register_routes(app):
    app.register_blueprint(auth_bp)

    # Principal
    @app.route("/")
    def home():
        productos = Producto.query.all()
        return render_template("index.html", productos=productos)

    # Validar la ruta static
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)
    
    # para ver la api con front
    @app.route("/api")
    def api():
        productos = Producto.query.all()
        for producto in productos:
            print(f"Producto en Flask: ID={producto.id}, Nombre={producto.nombre}")
        return render_template("api.html", productos=productos)
    
    # visualizar la documentación de la API
    @app.route("/documentacion")
    def documentacion():
        productos = Producto.query.all()
        return render_template("api_doc.html", productos=productos)

    # Ver la API completa de los productos
    @app.route('/productos_json', methods=['GET'])
    def obtener_productos():
        productos = Producto.query.all()
        return jsonify([producto.to_dict() for producto in productos])

    # Producto por ID
    @app.route('/producto/<int:producto_id>', methods=['GET'])
    def obtener_producto(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            return jsonify(producto.to_dict())
        return jsonify({"error": "Producto no encontrado"}), 404

    # Producto por Nombre
    @app.route('/producto/nombre/<string:nombre>', methods=['GET'])
    def obtener_producto_por_nombre(nombre):
        producto = Producto.query.filter_by(nombre=nombre).first()
        if producto:
            return jsonify(producto.to_dict())
        return jsonify({"error": "Producto no encontrado"}), 404

    # Producto por ID ver Calorias
    @app.route('/producto/<int:producto_id>/calorias', methods=['GET'])
    def consultar_calorias(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            return jsonify({"calorias": producto.calcular_calorias()})
        return jsonify({"error": "Producto no encontrado"}), 404

    # Producto por ID ver rentabilidad
    @app.route('/producto/<int:producto_id>/rentabilidad', methods=['GET'])
    def consultar_rentabilidad(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            return jsonify({"rentabilidad": producto.calcular_rentabilidad()})
        return jsonify({"error": "Producto no encontrado"}), 404

    # Producto por ID ver costo
    @app.route('/producto/<int:producto_id>/costo', methods=['GET'])
    def consultar_costo(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            return jsonify({"costo_produccion": producto.calcular_costo()})
        return jsonify({"error": "Producto no encontrado"}), 404

    # Producto por ID vender
    @app.route('/producto/<int:producto_id>/vender', methods=['POST'])
    def vender_producto(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            producto.vender()
            db.session.commit()
            return jsonify({"mensaje": "Producto vendido con éxito"})
        return jsonify({"error": "Producto no encontrado"}), 404

    # Ver API de los ingredientes completa
    @app.route('/ingredientes_json', methods=['GET'])
    def obtener_ingredientes():
        ingredientes = Ingrediente.query.all()
        return jsonify([ingrediente.to_dict() for ingrediente in ingredientes])

    # Ingrediente por ID
    @app.route('/ingrediente/<int:ingrediente_id>', methods=['GET'])
    def obtener_ingrediente(ingrediente_id):
        ingrediente = Ingrediente.query.get(ingrediente_id)
        if ingrediente:
            return jsonify(ingrediente.to_dict())
        return jsonify({"error": "Ingrediente no encontrado"}), 404

    # Ingrediente por nombre
    @app.route('/ingrediente/nombre/<string:nombre>', methods=['GET'])
    def obtener_ingrediente_por_nombre(nombre):
        ingrediente = Ingrediente.query.filter_by(nombre=nombre).first()
        if ingrediente:
            return jsonify(ingrediente.to_dict())
        return jsonify({"error": "Ingrediente no encontrado"}), 404

    # Ingrediente por ID ver si es saludable
    @app.route('/ingrediente/<int:ingrediente_id>/saludable', methods=['GET'])
    def verificar_saludable(ingrediente_id):
        ingrediente = Ingrediente.query.get(ingrediente_id)
        if ingrediente:
            return jsonify({"saludable": ingrediente.es_saludable()})
        return jsonify({"error": "Ingrediente no encontrado"}), 404

    # Producto por ID reabastecer
    @app.route('/producto/<int:producto_id>/reabastecer', methods=['POST'])
    def reabastecer_producto(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            producto.reabastecer()
            db.session.commit()
            return jsonify({"mensaje": "Producto reabastecido con éxito"})
        return jsonify({"error": "Producto no encontrado"}), 404

    # Producto por ID renovar
    @app.route('/producto/<int:producto_id>/renovar', methods=['POST'])
    def renovar_inventario(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            producto.renovar_inventario()
            db.session.commit()
            return jsonify({"mensaje": "Inventario renovado con éxito"})
        return jsonify({"error": "Producto no encontrado"}), 404