def planEntity(item) -> dict:
    return{
        "id_plan": item["id_plan"],
        "fecha_modificacion": item["fecha_modificacion"],
        "nombre": item["nombre"],
        "precio": item["precio"],
        "descripcion": item["descripcion"],
        "total_segundos": item["total_segundos"]

    }

def plansEntity(entity) -> list:
    return [planEntity(item) for item in entity]