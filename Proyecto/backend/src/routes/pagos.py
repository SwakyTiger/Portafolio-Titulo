from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from ..models.models import CreateCheckoutSession
import stripe

pagos = APIRouter()

@pagos.post("/create-checkout-session", tags=["pagos"])
def create_checkout_session(session_data: CreateCheckoutSession):
    try:
        # Crea el cliente en Stripe si no existe
        customer = stripe.Customer.create(
            email=session_data.user_email
        )

        # Crear la sesión de checkout para la suscripción
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': session_data.plan_name,
                    },
                    'recurring': {
                        'interval': 'month',  # Puede ser 'day', 'week', 'month', o 'year'
                    },
                    'unit_amount': session_data.price,
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url="http://localhost:8080/success",
            cancel_url="http://localhost:8080/cancel",
            customer=customer.id  # Asocia la sesión al cliente
        )
        return {"url": session.url}  # Asegúrate de devolver la URL
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=e.user_message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))





