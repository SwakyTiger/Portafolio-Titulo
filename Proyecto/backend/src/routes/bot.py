from fastapi import APIRouter, HTTPException, File, UploadFile,  Query
from src.config.db import conn
from ..schemas.schemas import usuariosEntity
import re

import subprocess
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='src/routes/.env') # Cargar el archivo .env

# Verificar el valor de GROQ_TOKEN
groq_token = os.getenv('GROQ_TOKEN')

if groq_token is None:
    raise HTTPException(status_code=500, detail="GROQ_TOKEN no está configurado.")

bot = APIRouter()
usuarios_collection = conn.alloxentric_db.usuario

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

@bot.get('/bot', tags=["bot"])
def find_all_usuarios():
    return usuariosEntity(conn.alloxentric_db.usuario.find())

@bot.get('/bot/{numero_telefono}', tags=["bot"])
def find_usuario(numero_telefono: str):
    # Verifica que el número tenga el formato esperado
    if not numero_telefono.startswith("+") or len(numero_telefono) < 5:
        raise HTTPException(status_code=400, detail="Número de teléfono inválido. Debe incluir el prefijo con '+'.")

    # 1. Crear un campo combinado y buscar el usuario
    usuario = conn.alloxentric_db.usuario.find_one(
        {"$expr": {"$eq": [{"$concat": ["$prefijo", {"$toString": "$numero_telefono"}]}, numero_telefono]}}
    )
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    id_usuario = usuario.get('id_usuario')  # Suponiendo que el campo _id es el id del usuario
    
    # 2. Obtener la suscripción del usuario utilizando el id_usuario
    suscripcion = conn.alloxentric_db.suscripciones.find_one({"id_usuario": id_usuario})
    
    # 3. Convertir los objetos de MongoDB a dicts si es necesario
    usuario_info = {
        "id_usuario": str(usuario["id_usuario"]),
        "username": usuario.get("username"),
        "nombre": usuario.get("nombre"),
        "apellido": usuario.get("apellido"),
        "numero_telefono": f"{usuario.get('prefijo')}{usuario.get('numero_telefono')}",
        "email": usuario.get("email")
    }

    # Verificar si la suscripción existe
    if suscripcion is None:
        suscripciones_info = {}
    else:
        suscripciones_info = {
            "id_plan": suscripcion.get("id_plan"),
            "estado": suscripcion.get("estado"),
            "creditos": suscripcion.get("creditos")
        }

    # 4. Retornar la información combinada
    return {
        "usuario": usuario_info,
        "suscripciones": suscripciones_info
    }


@bot.post("/transcribir-audio-2/", tags=["bot"])
async def transcribir_audio(audio_url: str):
    os.makedirs('temp', exist_ok=True)
    
    file_location = "temp/audio_url.wav"
    
    try:
        # Descargar el archivo de audio desde la URL
        response = requests.get(audio_url)
        response.raise_for_status()  # Lanza un error si la descarga falla
        
        # Guardar el archivo de audio
        with open(file_location, "wb") as f:
            f.write(response.content)

        # Verificar que el archivo no esté vacío
        if os.path.getsize(file_location) == 0:
            raise HTTPException(status_code=500, detail="El archivo de audio está vacío.")
        
        # Establecer la variable de entorno para el script de Node.js
        os.environ['GROQ_TOKEN'] = os.getenv('GROQ_TOKEN')

        # Llama al script de JavaScript para transcribir el audio
        result = subprocess.run(['node', 'transcripcion/transcribir.js', file_location], capture_output=True)

        # El resultado de la transcripción estará en result.stdout
        transcripcion = result.stdout.strip()
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error al ejecutar el script de transcripción: {result.stderr.strip()}")

        return {"transcripcion": transcripcion, "es_audio": True}
    
    except Exception as e:
        # Si ocurre un error, devolver un objeto que indique que es texto
        return {"detail": str(e), "es_audio": False}
    


@bot.post("/transcribir-audio/", tags=["bot"])
async def transcribir_audio(file: UploadFile = File(...)):
    # Crear el directorio 'temp' si no existe
    os.makedirs('temp', exist_ok=True)
    
    file_location = f"temp/{file.filename}"
    
    try:
        # Guardar el archivo de audio
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Llama al script de JavaScript para transcribir el audio
        result = subprocess.run(['node', 'transcripcion/transcribir.js', file_location], capture_output=True)

        # El resultado de la transcripción estará en result.stdout
        transcripcion = result.stdout.strip()
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail="Error al ejecutar el script de transcripción")

        return {"transcripcion": transcripcion}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@bot.put("/restar-creditos/{username}", tags=["bot"])
def restar_credito(username: str):
    # 1. Obtener el usuario con el número de teléfono
    usuario = conn.alloxentric_db.usuario.find_one({"username": username})
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    id_usuario = usuario.get('id_usuario')  # Suponiendo que el campo _id es el id del usuario
    
    # 2. Obtener la suscripción del usuario
    suscripcion = conn.alloxentric_db.suscripciones.find_one({"id_usuario": id_usuario})

    if not suscripcion:
        raise HTTPException(status_code=404, detail="Suscripción no encontrada")

    creditos = suscripcion.get('creditos')

    if creditos <= 0:
        raise HTTPException(status_code=400, detail="No hay suficientes créditos para restar")

    # 3. Restar un crédito
    new_creditos = creditos - 1

    # Actualizar la suscripción en la base de datos
    conn.alloxentric_db.suscripciones.update_one(
        {"id_usuario": id_usuario},
        {"$set": {"creditos": new_creditos}}
    )

    return {"mensaje": "Crédito restado exitosamente", "creditos_restantes": new_creditos}


@bot.post("/guardar-transcrito", tags=['bot'])
def guardar_transcrito(
    id_usuario: str = Query(..., description="Id del usuario"),
    username: str = Query(..., description="Nombre del usuario"),
    transcrito: str = Query(..., description="Texto transcrito")
):
    # 1. Obtener el texto transcrito
    fecha = datetime.now()  # Obtener la fecha y hora actual

    # 2. Crear el documento a insertar
    documento = {
        "id_usuario": id_usuario,
        "username": username,
        "data_transcrito": transcrito,
        "fecha_transcrito": fecha
    }

    # 3. Insertar el documento en la colección
    resultado = conn.alloxentric_db.historial_transcrito.insert_one(documento)

    # 4. Retornar una respuesta
    return {"mensaje": "Transcripción guardada exitosamente", "id": str(resultado.inserted_id)}


@bot.get('/separarMensaje_numero', tags=['bot'])
def separarMensaje_numero(mensaje: str):
    print(f"Se recibe mensaje para ser separado: {mensaje}")
    
    # Separar usando múltiples delimitadores
    mensaje_separado = re.split(r'\*\|\*|\* \| \*', mensaje)
    
    # Obtener el último elemento (número de teléfono)
    telefono = mensaje_separado[-1].strip()
    print(f"TELEFONO: {telefono}")
    
    return {'telefono': telefono}
@bot.get('/separarMensaje_msg', tags=['bot'])
def separarMensaje(mensaje: str):
    print(f"Se recibe mensaje para ser separado: {mensaje}")
    
    # Separar usando múltiples delimitadores
    mensaje_separado = re.split(r'\*\|\*|\* \| \*', mensaje)
    
    # Obtener el primer elemento (mensaje)
    mensaje_texto = mensaje_separado[0].strip()
    print(f"MENSAJE: {mensaje_texto}")
    
    return {'mensaje': mensaje_texto}