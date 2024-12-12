from fastapi import FastAPI, Request
from src.routes.plans import plans
from src.routes.ventas import ventas
from src.routes.usuario import usuarios
from src.routes.pagos import pagos
from src.routes.bot import bot
from src.routes.suscripcion import suscripciones
from src.routes.estadoSuscripcion import validarEstado
from src.routes.historial_transcrito import historial
from src.auth import keycloak_openid
from fastapi.middleware.cors import CORSMiddleware
import stripe
import os
import dotenv

dotenv.load_dotenv()

stripekey = os.getenv('API_STRIPE')
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None) #ajuste para que no se acceda a docs ni redocs
stripe.api_key = os.getenv('API_STRIPE')

app.include_router(plans)
app.include_router(ventas)
app.include_router(usuarios)
app.include_router(pagos)
app.include_router(validarEstado)
app.include_router(suscripciones)
app.include_router(bot)
app.include_router(historial)

# Middleware para agregar Keycloak al estado de la solicitud
@app.middleware("http")
async def add_keycloak_to_request(request: Request, call_next):
    request.state.keycloak = keycloak_openid  # Agregar Keycloak al estado
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://34.176.135.227:8080"],  # Cambia según la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
