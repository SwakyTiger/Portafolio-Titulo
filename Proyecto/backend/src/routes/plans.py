from fastapi import APIRouter, HTTPException, status, Response
from src.config.db import conn
from ..schemas.schemas import planEntity, plansEntity
from ..models.models import Plan
from starlette.status import HTTP_204_NO_CONTENT
from datetime import datetime
import stripe


plans = APIRouter()

#BUSCAR TODOS LOS PLANES
@plans.get('/plans', tags=["plans"])
def find_all_plans():
    return plansEntity(conn.alloxentric_db.planes.find())

#CREAR UN NUEVO PLAN
@plans.post('/plans', tags=["plans"])
async def create_plan(plan: Plan):
    # Valida que no exista un plan con el mismo código
    existing_plan = conn.alloxentric_db.planes.find_one({"id_plan": plan.id_plan})
    if existing_plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un plan con el código {plan.id_plan}. Por favor, usa un código diferente."
        )

    # Crea el producto en Stripe
    try:
        product = stripe.Product.create(
            name=plan.nombre,
            description=plan.descripcion,
        )
        
        # Crea el precio en Stripe
        price = stripe.Price.create(
            unit_amount=int(plan.precio),  # En centavos
            currency="usd",  # Cambia esto según sea necesario
            recurring={"interval": "month"},  # Cambia esto según el tipo de plan
            product=product.id,
        )
        
        # Guarda el nuevo plan en la base de datos
        new_plan = dict(plan)
        new_plan['stripe_product_id'] = product.id
        new_plan['stripe_price_id'] = price.id
        
        id = conn.alloxentric_db.planes.insert_one(new_plan).inserted_id

        # Retorna el plan creado
        plan = conn.alloxentric_db.planes.find_one({"_id": id})
        return planEntity(plan)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el plan en Stripe: {str(e)}"
        )
    
#BUSCAR UN PLAN POR SU ID
@plans.get('/plans/{id_plan}', tags=["plans"])
def find_plan(id_plan: str ):
    return planEntity(conn.alloxentric_db.planes.find_one({"id_plan": id_plan}))

#ACTUALIZAR PLANES
@plans.post('/plans/{id_plan}', tags=["plans"])
def update_plan(id_plan: str, plan: Plan):
    try:
        # Actualiza el producto en Stripe (nombre y descripción)
        stripe.Product.modify(
            plan.stripe_product_id,
            name=plan.nombre,
            description=plan.descripcion,
        )

        # Crea un nuevo precio en Stripe
        new_price = stripe.Price.create(
            product=plan.stripe_product_id,
            unit_amount=int(plan.precio),  # Stripe espera el monto en centavos
            recurring={"interval": "month"},
            currency="usd",
        )

        # Actualizar el stripe_price_id en el plan con el nuevo precio
        plan.stripe_price_id = new_price['id']

    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar el plan en Stripe: {e.user_message}"
        )

    # Actualizar el plan en MongoDB
    plan.fecha_modificacion = datetime.now().isoformat()  # Actualiza la fecha de modificación
    result = conn.alloxentric_db.planes.find_one_and_update(
        {"id_plan": id_plan},
        {"$set": dict(plan)},
        return_document=True
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El plan con id {id_plan} no existe."
        )

    return planEntity(result)

#ELIMINAR UN PLAN POR SU ID
@plans.delete('/plans/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["plans"])
def delete_plan(id: str):
    result = conn.alloxentric_db.planes.find_one_and_delete({"id_plan": id})
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El plan con id {id} no existe."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)