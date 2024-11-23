import pytest
import httpx

base_url = "http://localhost:8000"  

@pytest.mark.asyncio
async def test_find_all_suscripciones():
    """Prueba para obtener todas las suscripciones."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/suscripciones")
    assert response.status_code == 200
    assert isinstance(response.json()["ventas"], list)

@pytest.mark.asyncio
async def test_find_suscripcion_by_usuario_id():
    """Prueba para obtener suscripciones por ID de usuario."""
    id_usuario = "0eb3539d-a17a-4610-8dd2-79a489096f7b"  # ID de usuario existente para la prueba
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/suscripciones/{id_usuario}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_cancel_suscripcion():
    """Prueba para cancelar una suscripción."""
    id_suscripcion = "sub_1QMgCmJjkSMvs9wmmDmGF2Gr"  # ID de suscripción válida para la prueba
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/cancelar_suscripcion/{id_suscripcion}")
    assert response.status_code == 200
    assert response.json()["message"] == "Suscripción configurada para cancelarse al final del período"

@pytest.mark.asyncio
async def test_update_suscripcion():
    """Prueba para actualizar una suscripción."""
    subscriptionId = "sub_1QMgCmJjkSMvs9wmmDmGF2Gr"  # ID de suscripción válida para la prueba
    newPriceId = "price_1QFS0GJjkSMvs9wmfsvoTyx6"    # Nuevo ID de precio de Stripe válido
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/actualizar_suscripcion/{subscriptionId}/{newPriceId}")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Suscripción actualizada correctamente con créditos ajustados."

