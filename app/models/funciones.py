from calculadora import calcular_calorias, calcular_rentabilidad
from malteada import Malteada


def es_sano(calorias, es_vegetariano):
    if calorias < 100 or es_vegetariano:
        return True
    return False

# Función para calcular el costo de un producto
def calcular_costo_produccion(ingrediente1, ingrediente2, ingrediente3):
    total_costo = ingrediente1['precio'] + ingrediente2['precio'] + ingrediente3['precio']
    return total_costo