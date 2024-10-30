from fastapi import APIRouter
from src.config.db import conn
from ..schemas.schemas import usuarioEntity, usuariosEntity

bot = APIRouter()
usuarios_collection = conn.alloxentric_db.usuario

@bot.get('/bot', tags=["bot"])
def find_all_usuarios():
    return usuariosEntity(conn.alloxentric_db.usuario.find())

@bot.get('/bot/{numero_telefono}', tags=["bot"])
def find_usuario(numero_telefono: int ):
    return usuarioEntity(conn.alloxentric_db.usuario.find_one({"numero_telefono": numero_telefono}))

@bot.get('/suscripcion/{numero_telefono}', tags=["bot"])
def find_usuario(numero_telefono: int ):
    return usuarioEntity(conn.alloxentric_db.usuario.find_one({"numero_telefono": numero_telefono}))