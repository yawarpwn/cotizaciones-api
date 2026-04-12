# ============================================================
# Aquí definimos get_current_user(), una función que verifica
# el access token en cada request protegido.
#
# Se usa así en cualquier endpoint:
# def mi_endpoint(usuario = Depends(get_current_user)):
# ============================================================

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import verify_token

# OAuth2PasswordBearer le dice a FastAPI dónde buscar el token.
# tokenUrl="/auth/login" es solo para la documentación Swagger.
# En la práctica, el token viene en el header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),  # Extrae el token del header
    db: Session = Depends(get_db),
) -> User:
    """
    Dependencia que protege endpoints.
    Verifica el access token y retorna el usuario actual.

    Si el token es inválido o expiró, lanza un error 401.
    """
    payload = verify_token(token, type="access")

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
            # Este header le dice al cliente que debe autenticarse
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()

    if not user or not bool(user.is_active):
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")

    return user
