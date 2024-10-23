from fastapi import APIRouter, HTTPException, status, Response
from src.config.db import conn
from ..schemas.schemas import planEntity, plansEntity
from ..models.models import Plan
from starlette.status import HTTP_204_NO_CONTENT
import stripe


plans = APIRouter()

@plans.get('/plans', tags=["plans"])
def find_all_plans():
    return plansEntity(conn.alloxentric_db.planes.find())

@plans.post('/plans', tags=["plans"])
async def create_plan(plan: Plan):
    # Crea el producto en Stripe
    try:
        product = stripe.Product.create(
            name=plan.nombre,
            description=plan.descripcion,
        )
        
        # Crea el precio en Stripe
        price = stripe.Price.create(
            unit_amount=int(plan.precio * 100),  # En centavos
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
    
@plans.get('/plans/{id}', tags=["plans"])
def find_plan(id_plan: str ):
    return planEntity(conn.alloxentric_db.planes.find_one({"id_plan": id_plan}))

@plans.put('/plans/{id}', response_model=Plan, tags=["plans"])
def update_plan(id_plan: str, plan: Plan):
    result = conn.alloxentric_db.planes.find_one_and_update(
        {"id_plan": id_plan},
        {"$set": dict(plan)},
        return_document=True
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El plan con id {id} no existe."
        )
    return planEntity(result)


@plans.delete('/plans/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["plans"])
def delete_plan(id: str):
    result = conn.alloxentric_db.planes.find_one_and_delete({"id_plan": id})
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El plan con id {id} no existe."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


