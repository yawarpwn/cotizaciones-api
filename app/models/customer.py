# ============================================================
# Modelo de la tabla "clientes"
# ============================================================
# Un "modelo" en SQLAlchemy es una clase Python que representa
# una tabla en la base de datos.
#
# Cada atributo de la clase = una columna en la tabla.
# SQLAlchemy se encarga de crear la tabla y traducir
# operaciones Python a SQL automáticamente.
# ============================================================

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func  # func nos da funciones SQL como now()
from app.database import Base  # Importamos la Base que definimos antes


# Esta clase representa la tabla "clientes" en PostgreSQL.
# Al heredar de Base, SQLAlchemy sabe que debe tratarla como una tabla.
class Customer(Base):
    # __tablename__ define el nombre exacto de la tabla en la base de datos
    __tablename__ = "customers"

    # --- Columnas de la tabla ---

    # PRIMARY KEY: identificador único de cada cliente
    # index=True crea un índice para búsquedas más rápidas
    id = Column(Integer, primary_key=True, index=True)

    # Nombre del cliente, obligatorio (nullable=False)
    # String(100) = máximo 100 caracteres
    name = Column(String(100), nullable=False)

    # Email único por cliente
    # unique=True: no puede haber dos clientes con el mismo email
    # index=True: búsquedas por email serán rápidas
    email = Column(String(100), unique=True, index=True)

    # Teléfono opcional (por defecto nullable=True)
    phone = Column(String(20))

    # Dirección opcional
    address = Column(String(200))

    # Fecha de creación: se llena automáticamente cuando se crea el registro
    # server_default=func.now() le dice a PostgreSQL que use la hora actual
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Fecha de última actualización
    # onupdate=func.now() se actualiza automáticamente cada vez que
    # se modifica el registro
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
