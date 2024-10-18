from fastapi import FastAPI, HTTPException
from keycloak import KeycloakAdmin

app = FastAPI()

# Configura tu instancia de KeycloakAdmin
keycloak_admin = KeycloakAdmin(server_url="http://localhost:8081/",
                                username='admin_twa',
                                password='Adm2024.',
                                realm_name='Transcriptor',
                                client_id='transcriptor_alloxentric')
@app.get("/user/{username}")
async def get_user_info(username: str):
    try:
        user = keycloak_admin.get_user_id(username)
        if user:
            user_info = keycloak_admin.get_user(user)
            # Asumimos que los créditos están en un campo específico
            credits = user_info.get('attributes', {}).get('creditos', [0])[0]
            return {"username": username, "creditos": credits}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))