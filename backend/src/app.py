from fastapi import FastAPI
from src.routes.plans import plans
from src.routes.ventas import ventas
from src.routes.usuario import usuarios
from src.routes.pagos import pagos
from fastapi.middleware.cors import CORSMiddleware
import stripe

app = FastAPI()
stripe.api_key = "sk_test_51PpuxIJjkSMvs9wmF4duzY63l7tdSSHcgF4ydbTugtFpNfu4PXIPKbONR9zE3FuIUKxvkGHcJz1NPHLOCMtdyjI4001wdEchSc"


app.include_router(plans)
app.include_router(ventas)
app.include_router(usuarios)
app.include_router(pagos)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Cambia según la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
