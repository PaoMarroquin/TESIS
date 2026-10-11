from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import hash_password
from app.models.enums import RolNombre
from app.models.institucion import Rol, Usuario

def asegurar_roles(db: Session) -> None:
    existentes = {r.nombre for r in db.query(Rol).all()}
    for nombre in RolNombre:
        if nombre not in existentes:
            db.add(Rol(nombre=nombre))
    db.commit()

def asegurar_admin(db: Session) -> None:
    if not settings.ADMIN_DNI or not settings.ADMIN_PASSWORD:
        return
    rol = db.query(Rol).filter(Rol.nombre == RolNombre.super_admin).first()
    if db.query(Usuario).filter(Usuario.rol_id == rol.id).first():
        return  # ya existe un admin
    db.add(Usuario(
        dni=settings.ADMIN_DNI,
        nombres=settings.ADMIN_NOMBRES,
        apellidos=settings.ADMIN_APELLIDOS,
        email=settings.ADMIN_EMAIL or None,
        password_hash=hash_password(settings.ADMIN_PASSWORD),
        rol_id=rol.id,
    ))
    db.commit()