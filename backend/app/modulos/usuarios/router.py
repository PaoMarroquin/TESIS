from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.enums import RolNombre
from app.modulos.auth.dependencies import require_roles
from . import schemas, service

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    dependencies=[Depends(require_roles(RolNombre.super_admin))],
)

@router.post("", response_model=schemas.UsuarioCreado, status_code=status.HTTP_201_CREATED)
def crear(datos: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario, password = service.crear_usuario(db, datos)
    return schemas.UsuarioCreado(**service.a_out(usuario).model_dump(), password_temporal=password)

@router.get("", response_model=list[schemas.UsuarioOut])
def listar(
    institucion_id: Optional[UUID] = None,
    rol: Optional[RolNombre] = None,
    db: Session = Depends(get_db),
):
    return [service.a_out(u) for u in service.listar_usuarios(db, institucion_id, rol)]

@router.get("/{usuario_id}", response_model=schemas.UsuarioOut)
def obtener(usuario_id: UUID, db: Session = Depends(get_db)):
    return service.a_out(service.obtener_usuario(db, usuario_id))

@router.patch("/{usuario_id}", response_model=schemas.UsuarioOut)
def actualizar(usuario_id: UUID, datos: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    return service.a_out(service.actualizar_usuario(db, usuario_id, datos))

@router.post("/{usuario_id}/restablecer-password", response_model=schemas.PasswordTemporal)
def restablecer(usuario_id: UUID, db: Session = Depends(get_db)):
    return schemas.PasswordTemporal(password_temporal=service.restablecer_password(db, usuario_id))