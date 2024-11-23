import pytest
import httpx

base_url = "http://localhost:8000"  

@pytest.mark.asyncio
async def test_create_checkout_session():
    """Prueba para crear una sesión de checkout."""
    session_data = {
        "plan_name": "Plan 1",
        "price": "300",
        "user_email": "swakytiger@gmail.com",
        "user_name": "swakytiger",
        "id_usuario": "4db6175f-0300-4e95-a773-8e409fe34d84"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/create-checkout-session", json=session_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert data["url"].startswith("https://checkout.stripe.com")


