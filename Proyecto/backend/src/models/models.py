from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Plan(BaseModel):
    id_plan: str  # Stripe pide que sea en string para poder insertar la venta
    fecha_modificacion: str
    nombre: str
    precio: float
    descripcion: str
    total_segundos: int
    stripe_product_id: str = None  # ID del producto en Stripe
    stripe_price_id: str = None  # ID del precio en Stripe

class Venta(BaseModel):
    id_suscripcion: str
    id_usuario: str
    id_plan: str
    fecha_venta: datetime
    fecha_vencimiento: datetime
    total_pagado: int
    estado: str


class Suscripciones(BaseModel):
    id_suscripcion: str
    id_usuario: str
    id_plan: str
    fecha_venta: datetime
    fecha_vencimiento: datetime
    total_pagado: int
    estado: str
    
class Usuario(BaseModel):
    id_usuario: str
    username: str
    nombre: str
    apellido: str
    prefijo: str
    numero_telefono: int
    email: str

class CreateCheckoutSession(BaseModel):
    price: int
    plan_name: str
    user_email: str
    user_name: str
    id_usuario: str
