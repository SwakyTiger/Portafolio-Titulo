from fastapi import APIRouter, HTTPException, Request, Depends
from ..models.models import CreateCheckoutSession, Venta
from src.config.db import conn
from datetime import datetime
from bson import ObjectId
import stripe
import logging

suscripciones = APIRouter()
logging.basicConfig(level=logging.INFO)

@suscripciones.get("/suscripciones", tags=["suscripciones"])
async def obtener_suscripciones():
    try:
        # 1. Obtener todas las ventas del usuario
        suscripciones = list(conn.alloxentric_db.suscripciones.find())

        planes_list = {
            plan["id_plan"]: plan for plan in conn.alloxentric_db.planes.find({})}
        usuarios_list = {
            usuario["id_usuario"]: usuario for usuario in conn.alloxentric_db.usuario.find({})}

        total_clientes = len(set(sucripcion["id_usuario"] for sucripcion in suscripciones))

        response = []
        for sucripcion in suscripciones:
            plan_info = planes_list.get(sucripcion["id_plan"], {})
            usuario_info = usuarios_list.get(sucripcion["id_usuario"], {})
            response.append({"id_suscripcion": sucripcion["id_suscripcion"],
                            "id_usuario": sucripcion["id_usuario"], 
                            "id_plan": sucripcion["id_plan"],
                            "fecha_venta": sucripcion["fecha_venta"].isoformat(),
                            "fecha_vencimiento": sucripcion["fecha_vencimiento"].isoformat(),
                            "total_pagado": sucripcion["total_pagado"],
                            "estado": sucripcion["estado"],
                            "plan_info": {"nombre": plan_info.get("nombre", "Sin plan"),
                                        "precio": plan_info.get("precio", 0),
                                        "fecha_modificacion": plan_info.get("fecha_modificacion", "")},
                            "usuario_info": {"username": usuario_info.get("username", "Sin usuario"),
                                            "nombre": usuario_info.get("nombre", "Sin usuario"),
                                            "apellido": usuario_info.get("apellido", ""),
                                            "email": usuario_info.get("email", ""),
                                            "prefijo": usuario_info.get("prefijo", ""),
                                            "numero_telefono": usuario_info.get("numero_telefono", 0)}
            })

        return {"ventas": response, "total_clientes": total_clientes}
    except Exception as e:
        logging.error(f"Error obteniendo suscripciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo las suscripciones")
    
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
        # Obtener el plan nuevo y la cantidad de créditos asociados
        plan = conn.alloxentric_db.planes.find_one({"stripe_price_id": newPriceId})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan no encontrado")
        
        plan_id = plan.get("id_plan")
        total_pagado = plan.get("precio")
        creditos_nuevos = plan.get("creditos", 0)  # Créditos adicionales del nuevo plan
        
        # Recuperar la suscripción actual desde Stripe
        subscription = stripe.Subscription.retrieve(subscriptionId)
        
        # Verificar que la suscripción tenga elementos
        if not subscription.get("items") or not subscription["items"]["data"]:
            raise HTTPException(status_code=400, detail="No se encontraron elementos en la suscripción.")
        
        # Obtener el ID del item actual de la suscripción
        subscription_item_id = subscription['items']['data'][0]['id']

        # Calcular días usados y créditos consumidos en el plan actual
        fecha_inicio_unix = subscription['current_period_start']
        fecha_fin_unix = subscription['current_period_end']
        fecha_inicio = datetime.fromtimestamp(fecha_inicio_unix)
        fecha_fin = datetime.fromtimestamp(fecha_fin_unix)
        
        dias_totales = (fecha_fin - fecha_inicio).days
        dias_utilizados = (datetime.now() - fecha_inicio).days
        if dias_utilizados > dias_totales:
            dias_utilizados = dias_totales  # Evitar días negativos si la suscripción ya expiró
        print(f"Los dias totales son: {dias_totales} y los dias utilizados son: {dias_utilizados}")
        # Obtener los créditos del plan actual de la base de datos
        suscripcion_actual = conn.alloxentric_db.suscripciones.find_one({"id_suscripcion": subscriptionId})
        if not suscripcion_actual:
            raise HTTPException(status_code=404, detail="Suscripción no encontrada en la base de datos.")
        
        creditos_actuales = suscripcion_actual.get("creditos", 0)
        plan_actual_id = suscripcion_actual.get("id_plan")
        plan_actual = conn.alloxentric_db.planes.find_one({"id_plan": plan_actual_id})
        creditos_plan_actual = plan_actual.get("creditos", 0) if plan_actual else 0

        # Calcular los créditos consumidos en base a los días utilizados
        creditos_consumidos = int((dias_utilizados / dias_totales) * creditos_plan_actual)
        creditos_restantes = max(0, creditos_actuales - creditos_consumidos)  # Asegurarse de que no sea negativo
        print(f"Los creditos consumidos son: {creditos_consumidos} y los creditos restantes son: {creditos_restantes}")
        # Sumar los créditos del nuevo plan a los créditos restantes
        creditos_totales = creditos_restantes + creditos_nuevos
        print(f"Los creditos totales son: {creditos_totales}")
        # Actualizar los datos de la suscripción en la base de datos, incluyendo los créditos totales
        updated_subscription = stripe.Subscription.modify(
            subscriptionId,
            items=[{
                'id': subscription_item_id,
                'price': newPriceId,
            }],
            trial_end="now",  # Cobro inmediato
        )

        fecha_vencimiento = datetime.fromtimestamp(updated_subscription['current_period_end'])
        nuevo_estado = updated_subscription['status']

        result = conn.alloxentric_db.suscripciones.update_one(
            {"id_suscripcion": subscriptionId},
            {"$set": {
                "id_plan": plan_id,
                "estado": nuevo_estado,
                "total_pagado": total_pagado,
                "fecha_actualizacion": datetime.now(),
                "fecha_vencimiento": fecha_vencimiento,
                "creditos": creditos_totales  # Actualizar con los créditos acumulados
            }}
        )

        if result.modified_count == 1:
            # Obtener el id_usuario de la suscripción
            id_usuario = suscripcion_actual.get("id_usuario")
            if not id_usuario:
                raise HTTPException(status_code=404, detail="No se encontró el id_usuario en la suscripción.")
            
            # Insertar un nuevo registro en la colección ventas para el historial
            conn.alloxentric_db.ventas.insert_one({
                "id_suscripcion": subscriptionId,
                "id_usuario": id_usuario,
                "id_plan": plan_id,
                "total_pagado": total_pagado,
                "fecha_venta": datetime.now(),
                "fecha_vencimiento": fecha_vencimiento
            })

            return {"success": True, "message": "Suscripción actualizada correctamente con créditos ajustados.", "data": updated_subscription}
        else:
            raise HTTPException(status_code=404, detail="No se encontró la suscripción para actualizar en la base de datos")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))