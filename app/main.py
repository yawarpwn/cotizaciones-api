from fastapi import FastAPI

from app.database import Base, engine  # Para crear las tablas
from app.routers import customers  # El router de clientes
from app.routers import auth

# Base.metadata.create_all() lee todos los modelos que heredan de Base
# y crea sus tablas en PostgreSQL si aún no existen.
Base.metadata.create_all(bind=engine)

# Creamos la aplicación FastAPI
# Estos datos aparecen en la documentación automática (/docs)
app = FastAPI(
    title="Cotizaciones Tell Señales",
    description="API para gestión de clientes, cotizaciones y facturas",
    version="0.1.0",
)

# Registramos el routers a la app principal.
app.include_router(customers.router)
app.include_router(auth.router)


# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
def root():
    return {"mensaje": "API funcionando ✅"}
