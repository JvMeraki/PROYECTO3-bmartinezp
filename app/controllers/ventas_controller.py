from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.config.db import db
from app.models.base import Base
from app.models.detalle_venta import DetalleVenta
from app.models.producto import Producto
from app.models.venta import Venta

ventas_bp = Blueprint('ventas', __name__, url_prefix='/ventas')

@ventas_bp.route('/')
def ventas():
    ventas = Venta.query.all()
    productos = Producto.query.all()

    # Asegurar que los productos tengan precio
    productos_serializables = [
        {
            "id": producto.id,
            "nombre":producto.nombre,
            "precio": float(producto.precio_publico)
            }
        for producto in productos
    ]
    return render_template('ventas.html', ventas=ventas, productos=productos_serializables)

@ventas_bp.route('/crear', methods=['POST'])
def crear_venta():
    producto_ids = request.form.getlist("productos[]")  # Lista de IDs de productos
    cantidades = request.form.getlist("cantidades[]")  # Lista de cantidades

    if not producto_ids or not cantidades:
        flash("Error: Debes seleccionar al menos un producto y su cantidad", "danger")
        return redirect(url_for('ventas.ventas'))

    nueva_venta = Venta(fecha=datetime.now())
    db.session.add(nueva_venta)
    db.session.flush()  # Obtener el ID de la venta antes del commit

    total_venta = 0

    for i in range(len(producto_ids)):
        producto = Producto.query.get(producto_ids[i])
        if producto:
            cantidad = int(cantidades[i])

            for producto_ingrediente in producto.ingredientes:
                ingrediente = producto_ingrediente.ingrediente  # Accede al ingrediente real

                # Verificar la cantidad necesaria para bases (0.2 unidades por porción) y complementos (1 unidad por porción)
                cantidad_requerida = 0.2 if isinstance(ingrediente, Base) else 1
                if ingrediente.inventario < cantidad_requerida:
                    flash(f"¡Oh no! Nos hemos quedado sin {ingrediente.nombre} 😔", "danger")
                    return redirect(url_for('ventas.ventas'))

            # Reducir inventario de los ingredientes después de la venta
            for producto_ingrediente in producto.ingredientes:
                ingrediente = producto_ingrediente.ingrediente  # Accede al ingrediente real
                cantidad_requerida = 0.2 if isinstance(ingrediente, Base) else 1
                ingrediente.inventario -= cantidad_requerida

            # Calcular total del producto en la venta
            total = cantidad * producto.precio_publico
            total_venta += total

            # Crear detalle de venta
            detalle = DetalleVenta(
                venta_id=nueva_venta.id,
                producto_id=producto.id,
                cantidad=cantidad,
                total=total
            )
            db.session.add(detalle)

    nueva_venta.total = total_venta
    db.session.commit()

    flash("Venta realizada exitosamente", "success")
    return redirect(url_for('ventas.ventas'))