from fastapi import APIRouter, HTTPException
from ..models.models import CreateCheckoutSession
import stripe
import logging

pagos = APIRouter()
logging.basicConfig(level=logging.INFO)

@pagos.post("/create-checkout-session", tags=["pagos"])
def create_checkout_session(session_data: CreateCheckoutSession):
    try:
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
            success_url="http://localhost:8080/pagoRealizado?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8080/cancel",
            customer=customer.id,
            customer_creation='always',
            billing_address_collection='required',
            customer_email=session_data.user_email
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
        session = stripe.checkout.Session.retrieve(session_id)
        logging.info(f"Retrieved session: {session}")
        
        # Retrieve the payment intent to get the latest customer details
        payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
        logging.info(f"Retrieved payment intent: {payment_intent}")
        
        # Get the customer details
        customer = stripe.Customer.retrieve(payment_intent.customer)
        logging.info(f"Retrieved customer: {customer}")
        
        # Get the subscription details
        subscription = stripe.Subscription.retrieve(session.subscription)
        logging.info(f"Retrieved subscription: {subscription}")
        
        # Get the product details
        product = stripe.Product.retrieve(subscription.plan.product)
        logging.info(f"Retrieved product: {product}")
        
        return {
            "planName": product.name,
            "price": subscription.plan.amount / 100,
            "userName": customer.name if customer.name else "No disponible",
            "userEmail": customer.email
        }
    except stripe.error.StripeError as e:
        logging.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))