# Función para calcular la rentabilidad de un producto
def calcular_rentabilidad(precio_publico, ingredientes):
    # Calcular el costo total de los ingredientes
    costo_total = sum(ingrediente.precio for ingrediente in ingredientes)
    # Calcular la rentabilidad
    rentabilidad = precio_publico - costo_total
    return rentabilidad

# Función para calcular las calorías de un producto
def calcular_calorias(ingredientes, tipo_producto):
    if tipo_producto == 'Copa':
        # Para Copas, sumamos las calorias de los ingredientes y multiplicamos por 0.95
        calorias_totales = sum(ingrediente.calorias for ingrediente in ingredientes)
        calorias_totales *= 0.95
        return round(calorias_totales, 2)
    elif tipo_producto == "Malteada":
        # Para Malteadas, sumamos las calorias de los ingredientes y le agregamos las calorias de la crema chantilly
        calorias_totales = sum(ingrediente.calorias for ingrediente in ingredientes) + 200
        return calorias_totales
    else:
        raise ValueError("Tipo de producto no reconocido.")