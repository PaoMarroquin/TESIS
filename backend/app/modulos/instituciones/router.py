from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.enums import RolNombre
from app.modulos.auth.dependencies import require_roles
from . import schemas, service

router = APIRouter(
    prefix="/instituciones",
    tags=["instituciones"],
    dependencies=[Depends(require_roles(RolNombre.super_admin))],
)


@router.post("", response_model=schemas.InstitucionOut, status_code=status.HTTP_201_CREATED)
def crear(datos: schemas.InstitucionCreate, db: Session = Depends(get_db)):
    return service.crear_institucion(db, datos)


@router.get("", response_model=list[schemas.InstitucionOut])
def listar(db: Session = Depends(get_db)):
    return service.listar_instituciones(db)


@router.get("/{institucion_id}", response_model=schemas.InstitucionOut)
def obtener(institucion_id: UUID, db: Session = Depends(get_db)):
    return service.obtener_institucion(db, institucion_id)


@router.patch("/{institucion_id}", response_model=schemas.InstitucionOut)
def actualizar(institucion_id: UUID, datos: schemas.InstitucionUpdate, db: Session = Depends(get_db)):
    return service.actualizar_institucion(db, institucion_id, datos)


@router.post(
    "/{institucion_id}/anios",
    response_model=schemas.AnioAcademicoOut,
    status_code=status.HTTP_201_CREATED,
)
def crear_anio(institucion_id: UUID, datos: schemas.AnioAcademicoCreate, db: Session = Depends(get_db)):
    return service.crear_anio(db, institucion_id, datos)


@router.get("/{institucion_id}/anios", response_model=list[schemas.AnioAcademicoOut])
def listar_anios(institucion_id: UUID, db: Session = Depends(get_db)):
    return service.listar_anios(db, institucion_id)