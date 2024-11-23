import pytest
import httpx

base_url = "http://localhost:8000"  # URL base de tu API

@pytest.mark.asyncio
async def test_find_all_usuarios():
    """Prueba para obtener todos los usuarios."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/bot")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "id_usuario" in response.json()[0]
    assert "username" in response.json()[0]

@pytest.mark.asyncio
async def test_find_usuario():
    """Prueba para obtener un usuario específico."""
    email = "jondo@gmail.com"
    username = "jon.doe"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/bot/{email}/{username}")
    assert response.status_code == 200
    data = response.json()
    
    assert "usuario" in data
    assert "suscripciones" in data
    assert data["usuario"]["email"] == email
    assert data["usuario"]["username"] == username

@pytest.mark.asyncio
async def test_restar_credito():
    """Prueba para restar créditos de un usuario."""
    username = "jon.doe"
    
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{base_url}/restar-creditos/{username}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["mensaje"] == "Crédito restado exitosamente"
    assert "creditos_restantes" in data
    assert isinstance(data["creditos_restantes"], int)

@pytest.mark.asyncio
async def test_guardar_transcrito():
    """Prueba para guardar una transcripción."""
    params = {
        "id_usuario": "123",
        "username": "test_user",
        "transcrito": "Texto transcrito"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/guardar-transcrito", params=params)
    assert response.status_code == 200
    data = response.json()
    
    assert data["mensaje"] == "Transcripción guardada exitosamente"
    assert "id" in data
    assert isinstance(data["id"], str)
