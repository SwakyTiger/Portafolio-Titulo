from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import APIRouter
from datetime import datetime
from src.config.db import conn
import logging
import stripe

validarEstado = APIRouter()
logging.basicConfig(level=logging.INFO)

def validar_suscripciones():
    # Obtener todas las suscripciones cuya fecha de vencimiento haya pasado (sin importar su estado)
    suscripciones = conn.alloxentric_db.ventas.find({"fecha_venta": {"$lt": datetime.utcnow()}})

    for suscripcion in suscripciones:
        suscripcion_id = suscripcion["id_suscripcion"]
        try:
            # Obtener el estado actual de la suscripción desde Stripe
            subscription = stripe.Subscription.retrieve(suscripcion_id)

            # Si la suscripción está activa, actualizar su estado en MongoDB
            if subscription.status == "active":
                conn.alloxentric_db.ventas.update_one(
                    {"id_suscripcion": suscripcion_id},
                    {"$set": {"estado": "active"}}
                )
            elif subscription.status == "past_due":
                # Actualizar el estado como "past_due" si corresponde
                conn.alloxentric_db.ventas.update_one(
                    {"id_suscripcion": suscripcion_id},
                    {"$set": {"estado": "past_due"}}
                )
            elif subscription.status == 'canceled':
                # Actualizar el estado como "canceled" si corresponde
                conn.alloxentric_db.ventas.update_one(
                    {"id_suscripcion": suscripcion_id},
                    {"$set": {"estado": "canceled"}}
                )
            elif subscription.status == "unpaid":
                # Actualizar el estado como "unpaid" si corresponde
                conn.alloxentric_db.ventas.update_one(
                    {"id_suscripcion": suscripcion_id},
                    {"$set": {"estado": "unpaid"}}
                )

            else:
                # Si no está activa o en "past_due", actualizar como vencida
                conn.alloxentric_db.ventas.update_one(
                    {"id_suscripcion": suscripcion_id},
                    {"$set": {"estado": "vencida"}}
                )

        except Exception as e:
            logging.error(f"Error al validar la suscripción {suscripcion_id}: {str(e)}")


# Configurar el programador para ejecutar la validación todos los días
scheduler = BackgroundScheduler()
scheduler.add_job(validar_suscripciones, 'interval', days=10)
scheduler.start()

@validarEstado.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
