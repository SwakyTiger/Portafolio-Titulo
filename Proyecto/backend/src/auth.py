# auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8081",
    realm_name="Transcriptor",       # Nombre del realm utilizado
    client_id="transcriptor_alloxentric",    # ID del cliente 
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user_info = keycloak_openid.userinfo(token)
        if user_info:
            return user_info
    except:
        raise HTTPException(
            status_code=401,
            detail="No se pudieron validar las credenciales"
        )
