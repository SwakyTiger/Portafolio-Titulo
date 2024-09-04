from fastapi import APIRouter, HTTPException, status, Response
from src.config.db import conn
from ..schemas.schemas import usuarioEntity, usuariosEntity
from ..models.models import Usuario
from starlette.status import HTTP_204_NO_CONTENT


usuarios = APIRouter()
usuarios_collection = conn.alloxentric_db.usuario

@usuarios.get('/usuarios', tags=["Usuarios"])
def find_all_usuarios():
    return usuariosEntity(conn.alloxentric_db.usuario.find())

@usuarios.post('/usuarios', tags=["Usuarios"])
def create_usuario(usuario: Usuario):
    # Obtener el último ID de usuario
    last_user = usuarios_collection.find_one(sort=[("id_usuario", -1)])
    next_id = (last_user["id_usuario"] + 1) if last_user else 0

    # Verificar si el usuario ya existe (por email)
    existing_usuario = usuarios_collection.find_one({"email": usuario.email})
    if existing_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario con email {usuario.email} ya existe."
        )

    # Asignar el nuevo ID y crear el usuario
    usuario.id_usuario = next_id
    new_usuario = usuario.dict()
    usuarios_collection.insert_one(new_usuario)

    # Obtener el usuario recién creado
    created_usuario = usuarios_collection.find_one({"id_usuario": next_id})
    return usuarioEntity(created_usuario)

@usuarios.get('/usuarios/{id}', tags=["Usuarios"])
def find_usuario(id_plan: int ):
    return usuarioEntity(conn.alloxentric_db.usuario.find_one({"id_plan": id_plan}))

@usuarios.put('/usuarios/{id}', response_model=Usuario, tags=["Usuarios"])
def update_usuario(id: int, usuario: Usuario):
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
def delete_usuario(id: int):
    result = conn.alloxentric_db.usuario.find_one_and_delete({"id_plan": id})
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con id {id} no existe."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


