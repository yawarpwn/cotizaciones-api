# Centraliza todas las variables de configuración en un solo lugar.
# Lee los valores desde el archivo .env

from dotenv import load_dotenv
import os

load_dotenv()

# Clave secreta para firmar JWT
SECRET_KEY = os.getenv("SECRET_KEY")

# Algoritmo de firma del token. HS256 es el más común.
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Url de conexión: postgresql://usuario:contraseña@host:puerto/nombre_db
DATABASE_URL = os.getenv("DATABASE_URL")

# El access token dura poco tiempo (30 min) por seguridad.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# El refresh token dura más tiempo (7 días).
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
