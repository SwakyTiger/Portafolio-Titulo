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

@usuarios.get('/usuarios/{keycloak_id}')
async def get_usuario_by_keycloak_id(keycloak_id: str):
    usuario = conn.alloxentric_db.usuario.find_one({"id_usuario": keycloak_id})

    if usuario:
        return {"message": "Usuario encontrado", "id": str(usuario["_id"])}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@usuarios.post('/usuarios', status_code=status.HTTP_201_CREATED)
async def create_usuario(usuario: Usuario):
    if conn.alloxentric_db.usuario.find_one({"id_usuario": usuario.id_usuario}):
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    usuario_data = usuario.dict()
    result = conn.alloxentric_db.usuario.insert_one(usuario_data)
    return {"message": "Usuario guardado correctamente", "id": str(result.inserted_id)}

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


