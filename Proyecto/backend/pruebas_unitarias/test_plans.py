import pytest
import httpx
from unittest.mock import patch
from datetime import datetime

base_url = "http://localhost:8000"  
@pytest.mark.asyncio
async def test_find_all_plans():
    """Prueba para obtener todos los planes."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/plans")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_plan():
    
    """Prueba para crear un nuevo plan."""
    new_plan = {
        "id_plan": "8",
        "fecha_modificacion": "2024-11-22T12:00:00",  # Formato ISO 8601
        "nombre": "Plan Avanzado",
        "precio": 3000.0,
        "descripcion": "Incluye características premium",
        "creditos": 100,
    }
    # Mockear Stripe
    with patch("stripe.Product.create") as mock_product_create, patch("stripe.Price.create") as mock_price_create:
        mock_product_create.return_value = {"id": "prod_mock"}
        mock_price_create.return_value = {"id": "price_mock"}

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{base_url}/plans", json=new_plan)
        assert response.status_code == 200
        assert response.json()["id_plan"] == new_plan["id_plan"]

@pytest.mark.asyncio
async def test_find_plan_by_id():
    """Prueba para obtener un plan por su ID."""
    id_plan = "8"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/plans/{id_plan}")
    assert response.status_code == 200
    assert response.json()["id_plan"] == id_plan

@pytest.mark.asyncio
async def test_delete_plan():
    """Prueba para eliminar un plan por su ID."""
    plan_id = "8"
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{base_url}/plans/{plan_id}")
    assert response.status_code == 204

