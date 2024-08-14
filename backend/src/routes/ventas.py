from fastapi import APIRouter, HTTPException, status, Response
from src.config.db import conn
from ..schemas.schemas import ventaEntity, ventasEntity
from ..models.models import Venta
from starlette.status import HTTP_204_NO_CONTENT


ventas = APIRouter()

@ventas.get('/ventas', tags=["ventas"])
def find_all_ventas():
    return ventasEntity(conn.alloxentric_db.ventas.find())

@ventas.post('/ventas', tags=["ventas"])
def create_venta(venta: Venta):
    existing_venta = conn.alloxentric_db.ventas.find_one({"id_venta": venta.id_venta})
    if existing_venta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"la venta con id {venta.id_venta} ya existe."
        )
    new_venta = dict(venta)
    id = conn.alloxentric_db.ventas.insert_one(new_venta).inserted_id

    venta = conn.alloxentric_db.ventas.find_one({"_id": id})
    return ventaEntity(venta)

@ventas.get('/ventas/{id}', tags=["ventas"])
def find_venta(id_venta: int ):
    return ventaEntity(conn.alloxentric_db.ventas.find_one({"id_venta": id_venta}))

@ventas.put('/ventas/{id}', response_model=Venta, tags=["ventas"])
def update_venta(id: int, venta: Venta):
    result = conn.alloxentric_db.ventas.find_one_and_update(
        {"id_venta": id},
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
def delete_venta(id: int):
    result = conn.alloxentric_db.ventas.find_one_and_delete({"id_venta": id})
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La venta con id {id} no existe."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


