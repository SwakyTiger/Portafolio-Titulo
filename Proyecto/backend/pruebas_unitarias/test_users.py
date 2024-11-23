import pytest
import httpx
from unittest.mock import patch

base_url = "http://localhost:8000"  

@pytest.mark.asyncio
async def test_find_all_usuarios():
    """Prueba para obtener todos los usuarios."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/usuarios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_usuario():
    """Prueba para crear un nuevo usuario."""
    new_usuario = {
        "id_usuario": "888",
        "username": "Test1",
        "nombre": "Juan",
        "apellido": "Pruebas",
        "prefijo": "+56",
        "numero_telefono": "123456789",
        "email": "juan@gmail.com"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/usuarios", json=new_usuario)
    
    assert response.status_code == 201
    assert response.json()["message"] == "Usuario guardado correctamente"
    assert response.json()["id"]  # Verifica que se devuelve un ID

@pytest.mark.asyncio
async def test_find_usuario_by_keycloak_id():
    """Prueba para obtener un usuario por su ID de Keycloak."""
    keycloak_id = "0eb3539d-a17a-4610-8dd2-79a489096f7b" # keycloak id valida para realizar la prueba, se coloca asi debido a que normalmente se obtiene a traves de token en web(por quien se loguea)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/usuarios/{keycloak_id}")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Usuario encontrado"
    assert response.json()["id"]  # Verifica que se devuelve un ID

@pytest.mark.asyncio
async def test_update_usuario():
    """Prueba para actualizar un usuario por su ID."""
    update_data = {
        "id_usuario": "888",
        "nombre": "Juan",
        "apellido": "Pruebas",
        "prefijo": "+56",
        "numero_telefono": "87654321",
        "email": "juan@gmail.com",
        "username": "Test1",
    }

    usuario_id = "888"
    
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{base_url}/usuarios/{usuario_id}", json=update_data)
    
    assert response.status_code == 200
    assert response.json()["nombre"] == update_data["nombre"]
    assert response.json()["apellido"] == update_data["apellido"]

@pytest.mark.asyncio
async def test_delete_usuario():
    """Prueba para eliminar un usuario por su ID."""
    usuario_id = "888"
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{base_url}/usuarios/{usuario_id}")
    
    assert response.status_code == 204
