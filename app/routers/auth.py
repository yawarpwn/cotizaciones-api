from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    RefreshRequest,
    TokenResponse,
)
from app.core.security import (
    verify_password,
    verify_token,
    create_access_token,
    create_refresh_token,
    hash_password,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    print("data", data)
    # Verificamos que el email no esté ya registrado
    user = db.query(User).filter(User.email == data.email).first()
    print("user:", user)

    if user:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")

    # Hasheamos la contraseña ANTES de guardarla en la DB
    password_hash = hash_password(data.password)

    # Creamos el usuario con el hash, no con la contraseña original
    new_user = User(
        name=data.name,
        email=data.email,
        password_hash=password_hash,
        role=data.role,
        avatar=data.avatar,
    )

    print("new user", new_user)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    print("user: ", user)

    # Verificamos que usuario exista y que la contraseña se correcta
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrecto")

    # Verificamos que el usuario este activo
    if not bool(user.is_active):
        raise HTTPException(status_code=401, detail="El usuario no esta activo")

    # "sub" (subject) es el campo estándar para identificar al usuario.
    payload = {"sub": user.email, "user_id": user.id}

    # creamos ambos tokens
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    # Verificamos que el refresh token sea valido
    payload = verify_token(data.refresh_token, "refresh")

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Refresh token inválido o expirado. Inicia session nuevamente",
        )

    # Extraemos el email del payload del token
    email = payload.get("sub")

    # Verificamos que el usuario aún exista y esté activo
    user = db.query(User).filter(User.email == email).first()

    if not user or not bool(user.is_active):
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")

    # Creamos un nuevo par de tokens
    new_payload = {"sub": user.email, "user_id": user.id}
    new_access_token = create_access_token(new_payload)
    new_refresh_token = create_access_token(new_payload)

    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)
