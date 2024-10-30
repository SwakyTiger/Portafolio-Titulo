from fastapi import APIRouter, HTTPException, Request, Depends
from ..models.models import CreateCheckoutSession, Venta
from src.config.db import conn
from datetime import datetime
from bson import ObjectId
import stripe
import logging

suscripciones = APIRouter()
logging.basicConfig(level=logging.INFO)
    
@suscripciones.get("/suscripciones/{id_usuario}", tags=["suscripciones"])
async def obtener_suscripciones(id_usuario: str):
    try:
        # 1. Obtener todas las ventas del usuario
        suscripciones = list(conn.alloxentric_db.suscripciones.find({"id_usuario": id_usuario}))
        
        # 2. Para cada venta, obtener los detalles del plan correspondiente
        for suscripcion in suscripciones:
            id_plan = suscripcion.get("id_plan")
            if id_plan:  # Si existe un id_plan en la venta
                plan = conn.alloxentric_db.planes.find_one({"id_plan": id_plan})
                if plan:
                    suscripcion["nombre_plan"] = plan["nombre"]  # Añadir el nombre del plan a la venta
                    print(suscripcion["nombre_plan"])
                else:
                    suscripcion["nombre_plan"] = "Plan desconocido"  # En caso de no encontrar el plan
            else:
                suscripcion["nombre_plan"] = "Plan no especificado"

        return list(suscripciones)
    except Exception as e:
        logging.error(f"Error obteniendo suscripciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo las suscripciones")

@suscripciones.post("/cancelar_suscripcion/{id_suscripcion}", tags=["suscripciones"])
async def cancelar_suscripcion(id_suscripcion: str):
    try:
        # 1. Configurar la suscripción para que se cancele al final del período
        suscripcion_stripe = stripe.Subscription.modify(
            id_suscripcion,
            cancel_at_period_end=True  # Establece la cancelación al final del período
        )

        # 2. Actualizar el estado de la suscripción en la base de datos
        result = conn.alloxentric_db.suscripciones.update_one(
            { "id_suscripcion": id_suscripcion},
            {"$set": {"estado": "cancel_at_period_end"}}
        )
        
        if result.modified_count == 1:
            return {"message": "Suscripción configurada para cancelarse al final del período"}
        else:
            raise HTTPException(status_code=404, detail="No se encontró la suscripción para cancelar")

    except Exception as e:
        logging.error(f"Error cancelando suscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error cancelando la suscripción")

@suscripciones.post("/actualizar_suscripcion/{subscriptionId}/{newPriceId}", tags=["suscripciones"])
async def actualizar_suscripcion(subscriptionId: str, newPriceId: str):
    try:
        # Obtener el plan actual y precio para validaciones
        plan = conn.alloxentric_db.planes.find_one({"stripe_price_id": newPriceId})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan no encontrado")
        
        plan_id = plan.get("id_plan")
        total_pagado = plan.get("precio")
        
        # Recuperar la suscripción desde Stripe
        subscription = stripe.Subscription.retrieve(subscriptionId)
        
        # Asegurarse de que la suscripción tenga items
        if not subscription.get("items") or not subscription["items"]["data"]:
            raise HTTPException(status_code=400, detail="No se encontraron elementos en la suscripción.")
        
        # Obtener el ID del item actual de la suscripción
        subscription_item_id = subscription['items']['data'][0]['id']

        # Realizar el cobro inmediatamente y otorgar prorrateo para simular los 3 días de prueba
        updated_subscription = stripe.Subscription.modify(
            subscriptionId,
            items=[{
                'id': subscription_item_id,
                'price': newPriceId,
            }],
            trial_end="now",  # Cobro inmediato
            proration_behavior='create_prorations'  # Prorrateo para ajustar el precio
        )

        # Actualizar la base de datos con el nuevo plan y estado
        nuevo_estado = updated_subscription['status']
        
        result = conn.alloxentric_db.suscripciones.update_one(
            {"id_suscripcion": subscriptionId},
            {"$set": {
                "id_plan": plan_id,
                "estado": nuevo_estado,
                "total_pagado": total_pagado,
                "fecha_actualizacion": datetime.now()
            }}
        )

        if result.modified_count == 1:
            fecha_vencimiento = datetime.fromtimestamp(updated_subscription['current_period_end'])
            # Obtener el id_usuario de la colección suscripciones
            subscription_data = conn.alloxentric_db.suscripciones.find_one({"id_suscripcion": subscriptionId})
            if not subscription_data:
                raise HTTPException(status_code=404, detail="Suscripción no encontrada para obtener el id_usuario.")
            
            id_usuario = subscription_data.get("id_usuario")
            # Insertar un nuevo registro en la colección ventas para guardar el historial de actualización de la suscripción
            conn.alloxentric_db.ventas.insert_one({
                "id_suscripcion": subscriptionId,
                "id_usuario": id_usuario,
                "id_plan": plan_id,
                "total_pagado": total_pagado,
                "fecha_venta": datetime.now(),
                "fecha_vencimiento": fecha_vencimiento,  # Fecha de fin de suscripción
                "fecha_actualizacion": datetime.now()
            })
            return {"success": True, "message": "Suscripción actualizada correctamente con cobro inmediato y 3 días de prueba.", "data": updated_subscription}
        else:
            raise HTTPException(status_code=404, detail="No se encontró la suscripción para actualizar en la base de datos")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))