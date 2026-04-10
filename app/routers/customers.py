from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db  # La función que nos da la sesión DB
from app.models.customer import Customer
from app.schemas.customer import (  # Los schemas de validación
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)

# Creamos el router
# - prefix="/clientes" : todos los endpoints empiezan con /clientes
# - tags=["Customers"]  : agrupa los endpoints en la documentación Swagger
router = APIRouter(prefix="/customers", tags=["Customers"])


# ============================================================
# POST /clientes/ - Crear un nuevo cliente
# ============================================================
# - response_model=CustomerResponse : define qué devuelve el endpoint
# - status_code=201 : código HTTP para "creado exitosamente"
# ============================================================
@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    cliente: CustomerCreate,  # Pydantic valida automáticamente el body
    db: Session = Depends(get_db),  # FastAPI inyecta la sesión de DB aquí
):
    # Verificamos si ya existe un cliente con ese email
    # db.query(Customer) = SELECT * FROM clientes
    # .filter(...)      = WHERE email = '...'
    # .first()          = LIMIT 1
    exists = db.query(Customer).filter(Customer.email == cliente.email).first()

    if exists:
        # HTTPException devuelve un error HTTP al cliente
        # status_code=400 significa "Bad Request" (petición incorrecta)
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # cliente.model_dump() convierte el schema Pydantic a un diccionario:
    # {"nombre": "Juan", "email": "juan@mail.com", ...}
    # **dict desempaqueta el diccionario como argumentos del constructor
    new_customer = Customer(**cliente.model_dump())

    db.add(new_customer)  # Prepara el INSERT (aún no lo ejecuta)
    db.commit()  # Ejecuta el INSERT en la base de datos
    db.refresh(
        new_customer
    )  # Recarga el objeto desde la DB (para obtener id, created_at, etc.)
    return new_customer


# ============================================================
# GET /clientes/ - Listar todos los clientes
# ============================================================
# - skip  : cuántos registros saltar (para paginación)
# - limit : cuántos registros devolver como máximo
# Ejemplo: GET /clientes/?skip=0&limit=10 → primera página
#          GET /clientes/?skip=10&limit=10 → segunda página
# ============================================================
@router.get("/", response_model=List[CustomerResponse])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # SELECT * FROM clientes OFFSET skip LIMIT limit
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers


# ============================================================
# GET /clientes/{customer_id} - Obtener un cliente por su ID
# ============================================================
# {customer_id} es un parámetro dinámico en la URL.
# Ejemplo: GET /clientes/5 → busca el cliente con id=5
# ============================================================
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,  # FastAPI extrae el id de la URL automáticamente
    db: Session = Depends(get_db),
):
    # SELECT * FROM clientes WHERE id = customer_id LIMIT 1
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        # 404 = "Not Found" (no encontrado)
        raise HTTPException(status_code=404, detail="Customer no encontrado")

    return customer


# ============================================================
# PUT /clientes/{customer_id} - Actualizar un cliente
# ============================================================
# Recibe solo los campos que se quieren actualizar.
# Si no se envía un campo, se deja como está.
# ============================================================
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    datos: CustomerUpdate,  # Los campos a actualizar (todos opcionales)
    db: Session = Depends(get_db),
):
    # Primero buscamos el cliente
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer no encontrado")

    # model_dump(exclude_unset=True) devuelve SOLO los campos que el usuario
    # envió en el request, ignorando los que no se enviaron.
    # Ejemplo: si solo envió {"telefono": "999"}, solo actualizamos telefono.
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        # setattr(objeto, "campo", valor) es equivalente a: objeto.campo = valor
        setattr(customer, campo, valor)

    db.commit()  # Ejecuta el UPDATE en la base de datos
    db.refresh(customer)
    return customer


# ============================================================
# DELETE /clientes/{customer_id} - Eliminar un cliente
# ============================================================
# status_code=204 significa "No Content" (éxito sin respuesta)
# ============================================================
@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Customer).filter(Customer.id == customer_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Customer no encontrado")

    db.delete(cliente)  # Prepara el DELETE
    db.commit()  # Ejecuta el DELETE en la base de datos
