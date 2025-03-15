from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.config.db import db
from app.models.copa import Copa
from app.models.ingrediente import Ingrediente, TipoIngrediente
from app.models.malteada import Malteada

ingredientes_bp = Blueprint("ingredientes", __name__)

@ingredientes_bp.route("/")
def listar_ingredientes():
    ingredientes = Ingrediente.query.all()
    return render_template("/ingredientes.html", ingredientes=ingredientes)

@ingredientes_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_ingrediente():
    tipos_ingrediente = TipoIngrediente.query.all()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = float(request.form.get('precio'))
        calorias = int(request.form.get('calorias'))
        inventario = float(request.form.get('inventario'))
        es_vegetariano = request.form.get('es_vegetariano') == '1'
        tipo_ingrediente_id = int(request.form.get('tipo_ingrediente_id'))

        nuevo_ingrediente = Ingrediente(
            nombre=nombre,
            precio=precio,
            calorias=calorias,
            inventario=inventario,
            es_vegetariano=es_vegetariano,
            tipo_ingrediente_id=tipo_ingrediente_id
        )

        db.session.add(nuevo_ingrediente)
        db.session.commit()
        flash("Ingrediente agregado correctamente", "success")
        return redirect(url_for("ingredientes.listar_ingredientes"))

    return render_template("/form_ingrediente.html", tipos_ingrediente=tipos_ingrediente)