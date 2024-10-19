from fastapi import APIRouter, HTTPException, status, Response
from src.config.db import conn
from ..schemas.schemas import planEntity, plansEntity
from ..models.models import Plan
from starlette.status import HTTP_204_NO_CONTENT


plans = APIRouter()

@plans.get('/plans', tags=["plans"])
def find_all_plans():
    return plansEntity(conn.alloxentric_db.planes.find())

@plans.post('/plans', tags=["plans"])
def create_plan(plan: Plan):
    existing_plan = conn.alloxentric_db.planes.find_one({"id_plan": plan.id_plan})
    if existing_plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El plan con id {plan.id_plan} ya existe."
        )
    new_plan = dict(plan)
    id = conn.alloxentric_db.planes.insert_one(new_plan).inserted_id

    plan = conn.alloxentric_db.planes.find_one({"_id": id})
    return planEntity(plan)

@plans.get('/plans/{id}', tags=["plans"])
def find_plan(id_plan: int ):
    return planEntity(conn.alloxentric_db.planes.find_one({"id_plan": id_plan}))

@plans.put('/plans/{id}', response_model=Plan, tags=["plans"])
def update_plan(id: str, plan: Plan):
    result = conn.alloxentric_db.planes.find_one_and_update(
        {"id_plan": id},
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


