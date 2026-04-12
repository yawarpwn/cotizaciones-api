from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt  # Para crear y verificar token
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import (
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    ALGORITHM,
)

# ============================================================
# CryptContext configura el algoritmo de hashing de contraseñas.
# bcrypt es el estándar recomendado actualmente.
# "deprecated=auto" actualiza automáticamente hashes antiguos.
# ============================================================
ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Convierte una contraseña en texto plano a un hash seguro.
    Ejemplo: "mi123" → "$2b$12$abc...xyz"
    """
    return ph.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    """
    Compara una contraseña en texto plano con su hash guardado.
    Retorna True si coinciden, False si no.
    bcrypt hace la comparación de forma segura internamente.
    """
    try:
        ph.verify(hash_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


def create_access_token(data: dict) -> str:
    """
    Crea un JWT de corta duración (access token).

    El access token se envía en cada request a la API.
    Contiene información del usuario (como su email o id).
    """

    data_copy = data.copy()  # Copiamos para no modificar el original

    # Calculamos cuándo expira el token
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # "exp" es un campo estándar de JWT que indica la expiración
    data_copy.update({"exp": expiration, "type": "access"})

    # jwt.encode() firma y codifica el token con nuestra clave secreta
    token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_refresh_token(data: dict) -> str:
    """
    Crea un JWT de larga duración (refresh token).

    El refresh token NO se usa para acceder a la API.
    Solo sirve para obtener un nuevo access token cuando expira.
    """

    data_copy = data.copy()

    expiration = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    data_copy.update({"exp": expiration, "type": "refresh"})

    token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str, type: str) -> dict | None:
    """
    Verifica y decodifica un token JWT.

    Retorna el payload (datos dentro del token) si es válido.
    Retorna None si el token es inválido o expiró.

    - tipo: "access" o "refresh" para verificar que sea el tipo correcto
    """

    try:
        # jwt.decode() verifica la firma y la expiración automáticamente
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verificamos que sea el tipo correcto de token
        if payload.get("type") != type:
            return None

        return payload
    except JWTError:
        # JWTError se lanza si el token es inválido, fue modificado, o expiró
        return None
