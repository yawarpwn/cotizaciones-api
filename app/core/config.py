# Centraliza todas las variables de configuración en un solo lugar.
# Lee los valores desde el archivo .env
# from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv
import os

load_dotenv()

# Clave secreta para firmar JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("La variable de entorno SECRET_KEY no está configurada.")
SECRET_KEY = SECRET_KEY

# Algoritmo de firma del token. HS256 es el más común.
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Url de conexión: postgresql://usuario:contraseña@host:puerto/nombre_db
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no está configurada.")
DATABASE_URL = DATABASE_URL

# El access token dura poco tiempo (30 min) por seguridad.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# El refresh token dura más tiempo (7 días).
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(env_file=".env")
#     # Clave secreta para firmar JWT
#     SECRET_KEY: str = SettingsConfigDict(env_prefix="_SECRET_KEY_")
#
#     # Algoritmo de firma del token. HS256 es el más común.
#     ALGORITHM: str = "HS256"
#     # Url de conexión: postgresql://usuario:contraseña@host:puerto/nombre_db
#     DATABASE_URL: str
#
#     # El access token dura poco tiempo (30 min) por seguridad.
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#
#     # El refresh token dura más tiempo (7 días).
#     REFRESH_TOKEN_EXPIRE_DAYS: int = 7
#
#
# settings = Settings()
