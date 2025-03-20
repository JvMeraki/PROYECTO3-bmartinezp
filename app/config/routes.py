import os

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   send_from_directory, url_for)
from flask_login import current_user, login_required

from app.config.db import db
from app.controllers.auth import auth_bp
from app.controllers.project_controller import project_blueprint
from app.models.producto import Producto


def register_routes(app):
    @app.route("/")
    def home():
        productos = Producto.query.all()
        return render_template("index.html", productos=productos)

    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(os.path.join(app.root_path, 'static'), filename)
    
    @app.route('/producto/<int:producto_id>', methods=['GET'])
    def obtener_producto(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            return jsonify(producto.to_dict())
        return jsonify({"error": "Producto no encontrado"}), 404    

    @app.route('/productos_json', methods=['GET'])
    def obtener_productos_json():
        productos = Producto.query.all()
        return jsonify([producto.to_dict() for producto in productos])
    
    @app.route("/api")
    def api():
        productos = Producto.query.all()
        for producto in productos:
            print(f"Producto en Flask: ID={producto.id}, Nombre={producto.nombre}")  # 🔹 Depuración
        return render_template("api.html", productos=productos)