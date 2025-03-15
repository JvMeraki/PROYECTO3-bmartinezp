import os

from flask import Blueprint, render_template

from app.config.db import db
from app.models.producto import Producto

project_blueprint = Blueprint("project", __name__, url_prefix="/")

@project_blueprint.route("/", methods = ["GET"])
def get_home():
    productos = Producto.query.all()
    return render_template("index.html", productos=productos)