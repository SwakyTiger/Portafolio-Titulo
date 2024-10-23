from fastapi import APIRouter
from src.config.db import conn
from ..schemas.schemas import usuarioEntity, usuariosEntity

bot = APIRouter()
usuarios_collection = conn.alloxentric_db.usuario

@bot.get('/bot', tags=["bot"])
def find_all_usuarios():
    return usuariosEntity(conn.alloxentric_db.usuario.find())

@bot.get('/bot/{username}', tags=["bot"])
def find_usuario(username: str ):
    return usuarioEntity(conn.alloxentric_db.usuario.find_one({"username": username}))