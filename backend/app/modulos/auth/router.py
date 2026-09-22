from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.institucion import Usuario
from app.modulos.auth import schemas, service
from app.modulos.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db),):
    usuario = service.authenticate_user(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},)
    access_token = create_access_token(data={"sub": str(usuario.id)})
    return schemas.TokenResponse(access_token=access_token)

@router.get("/me", response_model=schemas.UsuarioOut)
def me(usuario: Usuario = Depends(get_current_user)):
    return schemas.UsuarioOut(
        id=usuario.id,
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        email=usuario.email,
        rol=usuario.rol.nombre.value,
        institucion_id=usuario.institucion_id,
    )