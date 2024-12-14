from fastapi import APIRouter, HTTPException, status, Response
from src.config.db import conn
from ..schemas.schemas import usuarioEntity, usuariosEntity
from ..models.models import Usuario
from starlette.status import HTTP_204_NO_CONTENT
import requests

usuarios = APIRouter()
usuarios_collection = conn.alloxentric_db.usuario

KEYCLOAK_URL = "http://localhost:8081"
REALM = "Transcriptor"
CLIENT_ID = "admin-cli"
USERNAME = "aj8"  # Cambia esto por tu nombre de usuario
PASSWORD = "admin"  # Cambia esto por tu contraseña


def get_access_token():
    """Función para obtener un token de acceso de Keycloak."""
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
    payload = {
        "client_id": CLIENT_ID,
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Error al obtener el token:", response.status_code, response.text)
        return None

def fetch_events(token):
    """Función para obtener eventos de Keycloak."""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{KEYCLOAK_URL}/admin/realms/{REALM}/events", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener eventos:", response.status_code, response.text)
        return []

def process_events(events):
    """Función para procesar eventos y actualizar MongoDB."""
    for event in events:
        if event["type"] == "UPDATE_PROFILE":
            user_id = event["userId"]
            updated_telefono = event["details"].get("updated_Telefono")
            
            # Asegúrate de que el número de teléfono sea un entero
            if updated_telefono:
                try:
                    # Convierte a entero, eliminando cualquier caracter no numérico
                    updated_telefono_int = int(''.join(filter(str.isdigit, updated_telefono)))
                except ValueError:
                    print(f"Error: El número de teléfono '{updated_telefono}' no es válido.")
                    continue  # Saltar a la siguiente iteración

                # Actualiza el usuario sin agregar los campos innecesarios
                conn.alloxentric_db.usuario.update_one(
                    {"id_usuario": user_id},  # Asegúrate de que 'id_usuario' es el campo correcto
                    {"$set": {"numero_telefono": updated_telefono_int}}  # Actualiza como entero
                )
                print(f"Actualizado usuario {user_id} con nuevo número de teléfono {updated_telefono_int}")



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

@usuarios.put('/usuarios/{id}', response_model=Usuario, tags=["Usuarios"])
def update_usuario(id: str, usuario: Usuario):
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
def delete_usuario(id: str):
    result = conn.alloxentric_db.usuario.find_one_and_delete({"id_usuario": id})
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con id {id} no existe."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@usuarios.get('/monitorear-eventos', tags=["Monitoreo"])
def monitor_events():
    """Endpoint para monitorear eventos de Keycloak."""
    token = get_access_token()
    if token:
        events = fetch_events(token)
        process_events(events)
        return {"message": "Eventos procesados correctamente"}
    raise HTTPException(status_code=500, detail="Error al obtener el token de acceso")