# ============================================================
# Schemas de validación con Pydantic
# ============================================================
# Los "schemas" son clases que definen la forma y validación
# de los datos que entran y salen de la API.
#
# Diferencia entre Model y Schema:
# - Model (SQLAlchemy) = estructura de la tabla en la DB
# - Schema (Pydantic)  = estructura de los datos en la API
#
# Pydantic valida automáticamente los datos. Si alguien envía
# un email con formato incorrecto, Pydantic lo rechaza antes
# de que lleguemos a tocar la base de datos.
# ============================================================

from pydantic import BaseModel, EmailStr  # EmailStr valida formato de email
from datetime import datetime
from typing import Optional  # Optional = el campo puede ser None


# ============================================================
# ClienteBase contiene los campos comunes que se repiten
# en los otros schemas. Es la "base" de la que heredan los demás.
# ============================================================
class CustomerBase(BaseModel):
    name: str  # Obligatorio
    email: EmailStr  # Obligatorio y debe tener formato válido
    phone: Optional[str] = None  # Opcional, por defecto None
    address: Optional[str] = None  # Opcional, por defecto None


# ============================================================
# ClienteCreate se usa cuando se CREA un cliente (POST)
# Por ahora es igual a ClienteBase, pero en el futuro
# podríamos agregar campos extra solo para la creación
# (como contraseña, por ejemplo).
# ============================================================
class CustomerCreate(CustomerBase):
    pass  # "pass" significa que no agrega nada nuevo por ahora


# ============================================================
# ClienteUpdate se usa cuando se ACTUALIZA un cliente (PUT)
# Todos los campos son opcionales porque el usuario puede
# querer actualizar solo el teléfono, o solo el nombre, etc.
# ============================================================
class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


# ============================================================
# ClienteResponse se usa para las RESPUESTAS de la API.
# Es lo que el cliente (frontend, Postman, etc.) recibe.
# Incluye los campos de ClienteBase + id y fechas.
# ============================================================
class CustomerResponse(CustomerBase):
    id: int  # Lo genera la DB automáticamente
    created_at: datetime  # Lo genera la DB automáticamente
    updated_at: Optional[datetime] = None

    # Config le dice a Pydantic cómo comportarse
    class Config:
        # from_attributes=True permite que Pydantic lea datos
        # directamente desde un objeto SQLAlchemy (el modelo Cliente)
        from_attributes = True
