from fastapi import APIRouter, HTTPException, Request, Depends
from ..models.models import CreateCheckoutSession, Venta
from src.config.db import conn
from datetime import datetime
from bson import ObjectId
import stripe
import logging
from .auth import require_admin_role, require_common_or_admin_user , require_common_user


pagos = APIRouter()
logging.basicConfig(level=logging.INFO)

@pagos.post("/create-checkout-session", tags=["pagos"])
def create_checkout_session(session_data: CreateCheckoutSession):
    try:
        print(session_data)
        # Verificar si el usuario ya tiene una suscripción activa
        existing_subscription = conn.alloxentric_db.suscripciones.find_one({
            "id_usuario": session_data.id_usuario,  # Asegúrate de pasar el ID del usuario en session_data
            "estado": {"$in": ["active","cancel_at_period_end"]}
        })
        
        if existing_subscription:
            return HTTPException(
                status_code=400, 
                detail="El usuario ya tiene una suscripción activa."
            )
        customer = stripe.Customer.create(
            email=session_data.user_email
        )
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': session_data.plan_name,
                    },
                    'recurring': {
                        'interval': 'month',
                    },
                    'unit_amount': session_data.price,
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url="http://34.176.251.141:8080/pagoRealizado?session_id={CHECKOUT_SESSION_ID}", #URL ACA
            cancel_url="http://34.176.251.141:8080/cancel", #URL ACA
            customer=customer.id
        )
        
        return {"url": session.url}
    except stripe.error.StripeError as e:
        logging.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@pagos.get("/payment-details")
async def get_payment_details(session_id: str):
    logging.info(f"Received request for session_id: {session_id}")
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")

    try:
        # Recuperar la sesión de Stripe con el ID proporcionado
        session = stripe.checkout.Session.retrieve(session_id)
        logging.info(f"Retrieved session: {session}")
        
        # Recuperar la información del cliente
        customer = stripe.Customer.retrieve(session.customer)
        logging.info(f"Retrieved customer: {customer}")

        # Recuperar los elementos de línea del pago (planes comprados)
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        logging.info(f"Retrieved line items: {line_items}")

        # Aquí se asume que el nombre se pasó en el `metadata` de la sesión o del cliente
        user_name = customer.metadata.get("user_name") if customer.metadata else "No disponible"

        return {
            "planName": line_items.data[0].description if line_items.data else "No disponible",
            "price": session.amount_total / 100 if session.amount_total else 0,
            "userName": user_name,
            "userEmail": customer.email if customer.email else "No disponible"
        }
    except stripe.error.StripeError as e:
        logging.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def obtener_detalles_plan(plan_name: str) -> dict:
    """
    Función que obtiene el id y los créditos de un plan dado su nombre.
    """
    logging.info(f"Buscando el plan con nombre: {plan_name}")
    plan = conn.alloxentric_db.planes.find_one({"nombre": plan_name})
    if plan:
        logging.info(f"Plan encontrado: {plan}")
        return {
            "id_plan": str(plan["id_plan"]),
            "creditos": plan.get("creditos", 0)  # Obtiene los créditos del plan, por defecto 0
        }
    else:
        logging.warning(f"No se encontró el plan con nombre: {plan_name}")
        return None

    
# Ruta para registrar la venta
@pagos.post("/record-sale", tags=["pagos"])
async def record_sale(session_id: str, request: Request):
    try:
        # Obtener el token de autorización
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        token_type, token = auth_header.split()
        if token_type != "Bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")

        # Decodificar el token de Keycloak
        token_info = request.state.keycloak.decode_token(token)
        id_usuario = token_info.get("sub")

        # Verificar si ya existe una venta para esta sesión
        existing_sale = conn.alloxentric_db.ventas.find_one({"session_id": session_id})
        if existing_sale:
            raise HTTPException(
                status_code=400,
                detail=f"La venta para la sesión {session_id} ya existe."
            )

        # Obtener los detalles de la sesión de Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Obtener los line items de la sesión
        line_items = stripe.checkout.Session.list_line_items(session_id)
        if not line_items or not line_items.data:
            raise HTTPException(status_code=400, detail="No se encontraron artículos en la sesión")

        # Obtener el nombre del primer artículo (plan)
        plan_name = line_items.data[0].description
        logging.info(f"Nombre del plan obtenido desde Stripe: {plan_name}")

        # Obtener id y créditos del plan
        logging.info(f"Buscando detalles del plan para: {plan_name}")
        plan_details = obtener_detalles_plan(plan_name)
        if not plan_details:
            logging.error(f"No se encontró detalles del plan para el nombre: {plan_name}")
            raise HTTPException(status_code=404, detail=f"No se encontró detalles del plan para el nombre proporcionado: {plan_name}")
        
        id_plan = plan_details["id_plan"]
        creditos = plan_details["creditos"]
        logging.info(f"ID del plan encontrado: {id_plan}, Créditos: {creditos}")
        
        # Obtener el ID de la suscripción desde la sesión
        if hasattr(session, 'subscription'):
            suscripcion_id = session.subscription  # Asumir que session.subscription tiene el ID de la suscripción
        else:
            raise HTTPException(status_code=404, detail="No se encontró la suscripción en la sesión")

        # Obtener detalles de la suscripción desde Stripe
        suscripcion = stripe.Subscription.retrieve(suscripcion_id)
        fecha_vencimiento_unix = suscripcion.current_period_end  # Fecha de vencimiento en formato UNIX
        fecha_vencimiento = datetime.utcfromtimestamp(fecha_vencimiento_unix)  # Convertir a formato legible
        estado = suscripcion.get('status')

        # Crear el objeto de venta con un id_venta generado automáticamente
        venta = {
            "_id": str(ObjectId()),
            "id_suscripcion": suscripcion_id,  # ID de la suscripción
            "id_usuario": id_usuario if id_usuario else "No disponible",
            "id_plan": id_plan if id_plan else 0,  # id_plan ahora tendrá el valor correcto
            "fecha_venta": datetime.utcnow(),
            "fecha_vencimiento": fecha_vencimiento,
            "total_pagado": session.amount_total if session.amount_total else 0
        }
        suscripcion = {
            "_id": str(ObjectId()),
            "id_suscripcion": suscripcion_id,  # ID de la suscripción
            "id_usuario": id_usuario if id_usuario else "No disponible",
            "id_plan": id_plan if id_plan else 0,  # id_plan ahora tendrá el valor correcto
            "fecha_venta": datetime.utcnow(),
            "fecha_vencimiento": fecha_vencimiento,  # Registrar la fecha de vencimiento
            "total_pagado": session.amount_total if session.amount_total else 0,
            "creditos": creditos,
            "estado": estado  # Estado inicial
        }
        logging.info(f"Datos de venta a insertar: {venta}")

        existing_sale = conn.alloxentric_db.ventas.find_one({"session_id": session_id})
        if existing_sale:
            return {
                "message": "La venta ya fue registrada.",
                "data": existing_sale
            }
        else:
            conn.alloxentric_db.ventas.insert_one(venta)

        # Verificar si ya existe una suscripción con el mismo id_suscripcion
        existing_subscription = conn.alloxentric_db.suscripciones.find_one({"id_suscripcion": suscripcion_id})
        if existing_subscription:
             return {
                "message": "La suscripcion ya fue registrada.",
                "data": existing_subscription
            }
        else:
            conn.alloxentric_db.suscripciones.insert_one(suscripcion)

        # Insertar la venta en MongoDB
        
    except stripe.error.StripeError as e:
        logging.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Imprimir el tipo de error y mensaje completo para ayudar a la depuración
        logging.error(f"Unexpected error: {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")
