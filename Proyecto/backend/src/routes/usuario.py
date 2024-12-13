from fastapi import APIRouter, HTTPException, status, Response, Depends
from src.config.db import conn
from ..schemas.schemas import usuarioEntity, usuariosEntity
from ..models.models import Usuario
from starlette.status import HTTP_204_NO_CONTENT
import requests
from .auth import require_common_user, require_admin_role, require_common_or_admin_user

usuarios = APIRouter()
usuarios_collection = conn.alloxentric_db.usuario


@usuarios.get('/usuarios', tags=["Usuarios"])
def find_all_usuarios(current_user: dict = Depends(require_admin_role)):
    return usuariosEntity(conn.alloxentric_db.usuario.find())

@usuarios.get('/usuarios/{keycloak_id}', tags=["Usuarios"])
async def get_usuario_by_keycloak_id(keycloak_id: str, current_user: dict = Depends(require_common_or_admin_user)):
    usuario = conn.alloxentric_db.usuario.find_one({"id_usuario": keycloak_id})

    if usuario:
        return {"message": "Usuario encontrado", "id": str(usuario["_id"])}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@usuarios.post('/usuarios', status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
async def create_usuario(usuario: Usuario, current_user: dict = Depends(require_common_or_admin_user)):
    if conn.alloxentric_db.usuario.find_one({"id_usuario": usuario.id_usuario}):
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    usuario_data = usuario.dict()
    result = conn.alloxentric_db.usuario.insert_one(usuario_data)
    return {"message": "Usuario guardado correctamente", "id": str(result.inserted_id)}

@usuarios.put('/usuarios/{id}', response_model=Usuario, tags=["Usuarios"])
def update_usuario(id: str, usuario: Usuario, current_user: dict = Depends(require_common_or_admin_user)):
    result = conn.alloxentric_db.usuario.find_one_and_update(
        {"id_usuario": id},
        {"$set": dict(usuario)},
        return_document=True
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con id {id} no existe."
        )
    return usuarioEntity(result)

@usuarios.delete('/usuarios/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def delete_usuario(id: str, current_user: dict = Depends(require_admin_role)):
    result = conn.alloxentric_db.usuario.find_one_and_delete({"id_usuario": id})
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con id {id} no existe."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
