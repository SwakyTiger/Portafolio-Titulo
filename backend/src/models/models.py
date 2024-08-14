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
    fecha_venta: str
