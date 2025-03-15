from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.config.db import db
from app.models.ingrediente import Ingrediente
from app.models.producto import Producto
from app.models.producto_ingrediente import ProductoIngrediente

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/")
def listar_productos():
    productos = Producto.query.all()
    return render_template("/productos.html", productos=productos)

@productos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    ingredientes = Ingrediente.query.all()

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio_publico = float(request.form["precio_publico"])
        tipo = request.form["tipo"]
        ingredientes_seleccionados = request.form.getlist("ingredientes")

        # Validar si los campos están vacíos
        if not nombre or not precio_publico:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for("/form.html"))

        try:
            precio_publico = float(precio_publico)
        except ValueError:
            flash("El precio debe ser un número válido.", "danger")
            return redirect(url_for("/form.html"))
        
        if len(ingredientes_seleccionados) != 3:
            flash("Debes seleccionar exactamente 3 ingredientes", "danger")
            return render_template("/form.html", ingredientes=ingredientes)

        # Crear el producto sin el costo de producción aún calculado
        nuevo_producto = Producto(nombre=nombre, costo_produccion=0, precio_publico=precio_publico, tipo=tipo)
        db.session.add(nuevo_producto)
        db.session.commit()  # Se necesita un commit para obtener el ID del producto

        # Asociar ingredientes
        for ingrediente_id in ingredientes_seleccionados:
            producto_ingrediente = ProductoIngrediente(producto_id=nuevo_producto.id, ingrediente_id=int(ingrediente_id))
            db.session.add(producto_ingrediente)

        db.session.commit()  # Guardamos la relación antes de calcular el costo

        # Recalcular el costo de producción después de asignar los ingredientes
        nuevo_producto.costo_produccion = nuevo_producto.calcular_costo()
        db.session.commit()

        flash(f"Producto agregado con éxito. Costo de producción: {nuevo_producto.costo_produccion} pesos", "success")
        return redirect(url_for("productos.listar_productos"))

    return render_template("/form.html", ingredientes=ingredientes)

@productos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id): 
    producto = Producto.query.get_or_404(id)
    
    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.precio_publico = request.form["precio_publico"]
        db.session.commit()
        flash("Producto actualizado con éxito", "success")
        return redirect(url_for("productos.listar_productos"))
    
    return render_template("/form.html", producto=producto, ingredientes=Ingrediente.query.all())

@productos_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado con éxito", "success")
    return redirect(url_for("productos.listar_productos"))