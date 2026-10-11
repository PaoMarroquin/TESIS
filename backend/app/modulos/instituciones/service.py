from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.institucion import AnioAcademico, Institucion
from . import schemas


def crear_institucion(db: Session, datos: schemas.InstitucionCreate) -> Institucion:
    if db.query(Institucion).filter(Institucion.codigo_modular == datos.codigo_modular).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe una institución con ese código modular")
    inst = Institucion(**datos.model_dump())
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return inst


def listar_instituciones(db: Session) -> list[Institucion]:
    return db.query(Institucion).order_by(Institucion.nombre).all()


def obtener_institucion(db: Session, institucion_id: UUID) -> Institucion:
    inst = db.get(Institucion, institucion_id)
    if not inst:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Institución no encontrada")
    return inst


def actualizar_institucion(db: Session, institucion_id: UUID, datos: schemas.InstitucionUpdate) -> Institucion:
    inst = obtener_institucion(db, institucion_id)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(inst, campo, valor)
    db.commit()
    db.refresh(inst)
    return inst


def crear_anio(db: Session, institucion_id: UUID, datos: schemas.AnioAcademicoCreate) -> AnioAcademico:
    obtener_institucion(db, institucion_id)
    if db.query(AnioAcademico).filter_by(institucion_id=institucion_id, anio=datos.anio).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Ese año académico ya existe en la institución")
    # Solo un año activo por institución: el nuevo cierra al anterior
    for previo in db.query(AnioAcademico).filter_by(institucion_id=institucion_id, estado="activo"):
        previo.estado = "cerrado"
    nuevo = AnioAcademico(institucion_id=institucion_id, estado="activo", **datos.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_anios(db: Session, institucion_id: UUID) -> list[AnioAcademico]:
    obtener_institucion(db, institucion_id)
    return (
        db.query(AnioAcademico)
        .filter_by(institucion_id=institucion_id)
        .order_by(AnioAcademico.anio.desc())
        .all()
    )