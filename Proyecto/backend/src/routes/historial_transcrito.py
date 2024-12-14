from fastapi import APIRouter, HTTPException
from src.config.db import conn
from datetime import datetime
import logging

historial = APIRouter()

@historial.get("/historial-transcrito", tags=["historial"])
async def obtener_historial_transcrito(username: str):
    try:
        # 1. Obtener el usuario correspondiente al username
        usuario = conn.alloxentric_db.usuario.find_one({"username": username})
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # 2. Obtener todos los historiales transcritos del usuario
        historiales = list(conn.alloxentric_db.historial_transcrito.find({"id_usuario": usuario["id_usuario"]}))

        response = []
        for historial in historiales:
            response.append({
                "id_historial": str(historial["_id"]),  # Convertir ObjectId a str
                "id_usuario": historial["id_usuario"],
                "username": usuario["username"],
                "data_transcrito": historial["data_transcrito"],
                "fecha_transcrito": historial["fecha_transcrito"].isoformat() if isinstance(historial["fecha_transcrito"], datetime) else historial["fecha_transcrito"],
            })

        return {"historiales": response}
    except Exception as e:
        logging.error(f"Error obteniendo historiales transcritos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo los historiales transcritos")