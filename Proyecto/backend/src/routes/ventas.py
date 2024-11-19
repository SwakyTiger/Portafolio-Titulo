from fastapi import APIRouter, HTTPException, status, Response, Query
from typing import Optional, List
from src.config.db import conn
from ..schemas.schemas import ventaEntity, ventasEntity
from ..models.models import Venta
from starlette.status import HTTP_204_NO_CONTENT
from .prefijos_paises import prefijos_paises
from datetime import datetime
import logging


ventas = APIRouter()

@ventas.get('/ventas', tags=["ventas"])
async def get_ventas(year: Optional[int] = None, month: Optional[int] = None, estado: Optional[str] = Query(None)):
    try:
        query = {}
        if year and month:
            query["fecha_venta"] = {
                "$gte": datetime(year, month, 1),
                "$lt": datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            }
        elif year:
            query["fecha_venta"] = {
                "$gte": datetime(year, 1, 1),
                "$lt": datetime(year + 1, 1, 1)
            }
        elif month:
            # Esto requiere que tengas un año predeterminado, podrías omitirlo si no es práctico
            raise HTTPException(status_code=400, detail="El mes debe incluir el año.")


        
        ventas_list = list(conn.alloxentric_db.ventas.find(query))
        planes_list = {
            plan["id_plan"]: plan for plan in conn.alloxentric_db.planes.find({})}
        usuarios_list = {
            usuario["id_usuario"]: usuario for usuario in conn.alloxentric_db.usuario.find({})}

        total_clientes = len(set(venta["id_usuario"] for venta in ventas_list))

        response = []
        for venta in ventas_list:
            plan_info = planes_list.get(venta["id_plan"], {})
            usuario_info = usuarios_list.get(venta["id_usuario"], {})
            response.append({"id_suscripcion": venta["id_suscripcion"],
                            "id_usuario": venta["id_usuario"], 
                            "id_plan": venta["id_plan"],
                            "fecha_venta": venta["fecha_venta"].isoformat(),
                            "fecha_vencimiento": venta["fecha_vencimiento"].isoformat(),
                            "total_pagado": venta["total_pagado"],
                            "plan_info": {"nombre": plan_info.get("nombre", "Sin plan"),
                                        "precio": plan_info.get("precio", 0),
                                        "fecha_modificacion": plan_info.get("fecha_modificacion", "")},
                            "usuario_info": {"username": usuario_info.get("username", "Sin usuario"),
                                            "nombre": usuario_info.get("nombre", "Sin usuario"),
                                            "apellido": usuario_info.get("apellido", ""),
                                            "email": usuario_info.get("email", ""),
                                            "prefijo": usuario_info.get("prefijo", ""),
                                            "numero_telefono": usuario_info.get("numero_telefono", 0)}
            })
        return {"ventas": response, "total_clientes": total_clientes}
    except Exception as e:
        print(f"Error al obtener ventas: {e}")
        return {"error": str(e)}, 500

ventas.post('/ventas', tags=["ventas"])
def create_venta(venta: Venta):
    existing_venta = conn.alloxentric_db.ventas.find_one({"id_suscripcion": venta.id_suscripcion})
    if existing_venta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"la venta con id {venta.id_suscripcion} ya existe."
        )
    new_venta = dict(venta)
    id = conn.alloxentric_db.ventas.insert_one(new_venta).inserted_id

    venta = conn.alloxentric_db.ventas.find_one({"_id": id})
    return ventaEntity(venta)
@ventas.get('/ventas/{id}', tags=["ventas"])
def find_venta(id_venta: int ):
    return ventaEntity(conn.alloxentric_db.ventas.find_one({"id_venta": id_venta}))

@ventas.put('/ventas/{id}', response_model=Venta, tags=["ventas"])
def update_venta(id: str, venta: Venta):
    result = conn.alloxentric_db.ventas.find_one_and_update(
        {"id_suscripcion": id},
        {"$set": dict(venta)},
        return_document=True
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La venta con id {id} no existe."
        )
    return ventaEntity(result)


@ventas.delete('/ventas/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["ventas"])
def delete_venta(id: str):
    result = conn.alloxentric_db.ventas.find_one_and_delete({"id_venta": id})
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La venta con id {id} no existe."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


