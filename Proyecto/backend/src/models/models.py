from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Plan(BaseModel):
    id_plan: int
    fecha_modificacion: str
    nombre: str
    precio: float
    descripcion: str
    total_segundos: int

class Venta(BaseModel):
    id_suscripcion: int
    id_usuario: int
    id_plan: int
    fecha_venta: datetime
    fecha_vencimiento: datetime
    total_pagado: int

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
