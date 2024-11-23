import pytest
import httpx
from unittest.mock import patch

base_url = "http://localhost:8000"  

@pytest.mark.asyncio
async def test_find_all_ventas():
    """Prueba para obtener todas las ventas."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/ventas")
    assert response.status_code == 200
    assert isinstance(response.json()["ventas"], list)

