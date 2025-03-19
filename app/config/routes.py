import os

from flask import (Blueprint, flash, redirect, render_template,
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
    
