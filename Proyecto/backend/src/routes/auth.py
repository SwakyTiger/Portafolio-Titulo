# src/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import List
from pydantic import BaseModel

# Configuración de la clave pública y algoritmo
KEYCLOAK_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvSE34qSFCmc6Di1w1UjcgUYiit3NssvO8UbNW4fapvM8djvcfJ6Cn/JAboJLx8vtzrvCjFDsE7AnVAGnTCHb9lJtwXlX6codcc9vxhtgyUiyIwxzz2j57XpybYNF5xFUbegTYSGPGs4nz0pXMaZFdEuQP34h275vgCgXA/irpr0qxKdsUlhHstjT1BSQ7KRbamzAcwIp6+bwLYVDt16lrPBccIN8T72TCRa2ypxw1C53CpBWQEFqsrG4W7yTVyufZHmd3Jc1zQmU/hvkOTVySfhxy2Vs6biEDqxWsNSejINtnx8WKYpyJmXK/l7c6fNRK0Citg/0rIDXIppBtg0CZwIDAQAB
-----END PUBLIC KEY-----"""

ALGORITHM = "RS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: str
    roles: List[str]

# Función para obtener el usuario actual
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token usando la clave pública
        payload = jwt.decode(token, KEYCLOAK_PUBLIC_KEY, algorithms=[ALGORITHM], audience="account")
        username: str = payload.get("preferred_username")
        
        # Obtén los roles de resource_access
        resource_roles = payload.get("resource_access", {}).get("transcriptor_alloxentric", {}).get("roles", [])
        roles = payload.get("realm_access", {}).get("roles", []) + resource_roles
        
        # Verifica que el nombre de usuario no sea None
        if username is None:
            raise credentials_exception
    except JWTError as e:
        # Manejo específico para el error de expiración del token
        if "Signature has expired" in str(e):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        print(f"JWTError: {e}")  # Agrega un print para ver el error
        raise credentials_exception
    
    # Devuelve el usuario y sus roles
    return {"username": username, "roles": roles}

# Función para verificar si el usuario tiene el rol de admin
def require_admin_role(current_user: dict = Depends(get_current_user)):
    # Verifica si el rol 'admin' está en resource_access
    if "admin" not in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
# Función para verificar si el usuario es común (no admin)
def require_common_user(current_user: dict = Depends(get_current_user)):
    # Verifica si el rol 'admin' no está en resource_access
    if "admin" in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin users are not allowed here")
    
    # Si el usuario no tiene el rol de admin, se considera un usuario común
    return current_user

# Función para verificar si el usuario es admin o común (sin rol)
def require_common_or_admin_user(current_user: dict = Depends(get_current_user)):
    # Verifica si el rol 'admin' está en resource_access
    if "admin" in current_user.get("roles", []):
        return current_user  # Permitir acceso a administradores

    # Si el usuario no tiene rol, se considera un usuario común
    return current_user  # Permitir acceso a usuarios comunes (sin rol)