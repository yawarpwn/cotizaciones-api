# ============================================================
# SQLAlchemy es el ORM (Object Relational Mapper) que nos permite
# interactuar con la base de datos usando clases Python en lugar
# de escribir SQL directamente.
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL

# El "engine" es el motor de conexión a la base de datos.
# Es el objeto principal que SQLAlchemy usa para comunicarse con PostgreSQL.
engine = create_engine(DATABASE_URL)

# SessionLocal es una "fábrica" de sesiones.
# Cada vez que necesitemos hablar con la DB, crearemos una sesión desde aquí.
# - autocommit=False : los cambios no se guardan solos, hay que hacer commit()
# - autoflush=False  : no envía cambios a la DB hasta que se haga commit()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase padre de todos nuestros modelos (tablas).
# Cada modelo que creemos heredará de esta clase.
Base = declarative_base()


# ============================================================
# get_db() es una función especial llamada "dependencia" en FastAPI.
# FastAPI la llama automáticamente antes de cada endpoint que la necesite.
#
# Funciona así:
# 1. Crea una sesión de DB
# 2. La entrega al endpoint (yield)
# 3. Cuando el endpoint termina, cierra la sesión (finally)
#
# Esto garantiza que la sesión siempre se cierre, incluso si hay un error.
# ============================================================
def get_db():
    db = SessionLocal()  # Abrimos una nueva sesión
    try:
        yield db  # Entregamos la sesión al endpoint
    finally:
        db.close()  # Siempre cerramos la sesión al terminar
