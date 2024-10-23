#ESQUEMA DE PLANES
def planEntity(item) -> dict:
    return{
        "id_plan": item["id_plan"],
        "fecha_modificacion": item["fecha_modificacion"],
        "nombre": item["nombre"],
        "precio": item["precio"],
        "descripcion": item["descripcion"],
        "total_segundos": item["total_segundos"],
        "stripe_product_id": item["stripe_product_id"],
        "stripe_price_id": item["stripe_price_id"]

    }

def plansEntity(entity) -> list:
    return [planEntity(item) for item in entity]

#ESQUEMA DE VENTAS
def ventaEntity(item) -> dict:
    return{
        "id_suscripcion": item["id_suscripcion"],
        "id_usuario": item["id_usuario"],
        "id_plan": item["id_plan"],
        "fecha_venta": item["fecha_venta"],
        "fecha_vencimiento": item["fecha_vencimiento"],  # Se puede hacer opcional si al crear la venta inicial aún no tienes la fecha
        "total_pagado": item["total_pagado"],
        "estado": item["estado"]
    }

def ventasEntity(entity) -> list:
    return [ventaEntity(item) for item in entity]

#ESQUEMA DE USUARIOS
def usuarioEntity(item) -> dict:
    return{
        "id_usuario": item["id_usuario"],
        "username": item["username"],
        "nombre": item["nombre"],
        "apellido": item["apellido"],
        "prefijo": item["prefijo"],
        "numero_telefono": item["numero_telefono"],
        "email": item["email"]

    }

def usuariosEntity(entity) -> list:
    return [usuarioEntity(item) for item in entity]