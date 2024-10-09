from fastapi import APIRouter,Request, HTTPException
import stripe
from bson import ObjectId
from datetime import datetime
from src.config.db import conn

stripe_router = APIRouter()
# Configuración de la clave secreta de Stripe
stripe.api_key = "sk_test_51PpuxIJjkSMvs9wmF4duzY63l7tdSSHcgF4ydbTugtFpNfu4PXIPKbONR9zE3FuIUKxvkGHcJz1NPHLOCMtdyjI4001wdEchSc"
endpoint_secret = "whsec_7cc719afedc69ad72f6ce6baa2dc5cf798faccf526aec98c1e2641816ad7d352"


@stripe_router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    print("Webhook recibido")  # Log para saber si el webhook fue llamado correctamente

    try:
        # Verificar la firma del webhook para asegurar la autenticidad
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        print(f"Evento recibido: {event['type']}")  # Log del tipo de evento recibido
    except ValueError as e:
        print(f"Error de payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        print(f"Error de firma: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Manejar eventos específicos de Stripe
    if event["type"] == "invoice.payment_succeeded":
        # Obtener la información de la factura
        invoice = event["data"]["object"]
        print(f"Factura recibida: {invoice}")  # Verificar contenido de la factura
        customer_id = invoice.get("customer", "No disponible")
        subscription_id = invoice.get("subscription", "No disponible")
        amount_paid = invoice.get("amount_paid", 0) / 100  # Convertir a formato decimal
        #currency = invoice.get("currency", "No disponible")

        # Recuperar información adicional del cliente y la suscripción
        try:
            customer = stripe.Customer.retrieve(customer_id)
            subscription = stripe.Subscription.retrieve(subscription_id)
            print(f"Cliente: {customer}, Suscripción: {subscription}")  # Verificar cliente y suscripción recuperados
        except Exception as e:
            print(f"Error al recuperar cliente o suscripción: {e}")
            raise HTTPException(status_code=500, detail="Error al recuperar cliente o suscripción")

        # Definir la venta con los campos requeridos para tu base de datos
        venta = {
            "_id": str(ObjectId()),  # Generar un ObjectId automáticamente
            "id_usuario": customer_id if customer_id else "No disponible",
            "id_plan": subscription["plan"]["id"] if subscription else 0,
            "fecha_venta": datetime.utcnow(),  # Fecha actual en UTC
            "total_pagado": amount_paid,
            #"moneda": currency,
            #"tipo_venta": "renovacion"  # Identificar como renovación
        }

        print(f"Venta a insertar: {venta}")  # Verificar la venta que se va a insertar

        try:
            # Insertar en la colección de ventas
            conn.alloxentric_db.ventas.insert_one(venta)
            print(f"Venta creada correctamente: {venta}")
        except Exception as e:
            print(f"Error al insertar la venta en la base de datos: {e}")
            raise HTTPException(status_code=500, detail="Error al insertar la venta en la base de datos")

    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        print(f"Suscripción actualizada: {subscription.id}")

    elif event["type"] == "invoice.upcoming":
        invoice = event["data"]["object"]
        print(f"Próxima renovación de la suscripción: {invoice.subscription}")

    # Responder a Stripe con un 200 OK
    return {"status": "success"}
