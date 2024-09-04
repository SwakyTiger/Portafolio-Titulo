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
    id_venta: int
    id_usuario: int
    id_plan: int
    fecha_venta: datetime

class Usuario(BaseModel):
    id_usuario: Optional[int]
    nombre: str
    apellido: str
    prefijo: str
    numero_telefono: int
    email: str
    pwd: str

class CreateCheckoutSession(BaseModel):
    price: int
    plan_name: str
    user_email: str
