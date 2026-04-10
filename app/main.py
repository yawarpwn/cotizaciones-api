# ============================================================
# Este es el archivo que uvicorn ejecuta para levantar el servidor.
# Aquí se configura la app y se registran todos los routers.
# ============================================================

from fastapi import FastAPI

from app.database import Base, engine  # Para crear las tablas
from app.routers import customers  # El router de clientes

#
# Base.metadata.create_all() lee todos los modelos que heredan de Base
# y crea sus tablas en PostgreSQL si aún no existen.
# Es equivalente a ejecutar CREATE TABLE IF NOT EXISTS ...
# Cuando agreguemos cotizaciones y facturas, sus tablas también
# se crearán aquí automáticamente.
Base.metadata.create_all(bind=engine)

# Creamos la aplicación FastAPI
# Estos datos aparecen en la documentación automática (/docs)
app = FastAPI(
    title="Cotizaciones Tell Señales",
    description="API para gestión de clientes, cotizaciones y facturas",
    version="0.1.0",
)

# Registramos el router de clientes en la app principal.
# Todos los endpoints de customers.py quedan disponibles.
# Cuando agreguemos más módulos, haremos lo mismo:
# app.include_router(cotizaciones.router)
# app.include_router(facturas.router)
app.include_router(customers.router)


# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
def root():
    return {"mensaje": "API funcionando ✅"}
