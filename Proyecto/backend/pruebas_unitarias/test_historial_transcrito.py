import pytest
import httpx

base_url = "http://localhost:8000"  # URL base de tu API

@pytest.mark.asyncio
async def test_obtener_historial_transcrito():
    """Prueba  para obtener el historial transcrito de un usuario."""
    username = "jon.doe"  # Asegúrate de que este usuario exista en la base de datos
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/historial-transcrito", params={"username": username})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "historiales" in data
    assert isinstance(data["historiales"], list)
    if data["historiales"]:  # Si hay historiales, comprobar campos clave
        assert "id_historial" in data["historiales"][0]
        assert "id_usuario" in data["historiales"][0]
        assert "username" in data["historiales"][0]
        assert "data_transcrito" in data["historiales"][0]
        assert "fecha_transcrito" in data["historiales"][0]
