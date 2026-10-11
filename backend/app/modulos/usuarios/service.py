import secrets
import string
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.enums import RolNombre
from app.models.institucion import Docente, Institucion, Rol, Usuario
from . import schemas

_ALFABETO = "".join(c for c in string.ascii_letters + string.digits if c not in "O0Il1")

def generar_password(longitud: int = 10) -> str:
    return "".join(secrets.choice(_ALFABETO) for _ in range(longitud))

def a_out(u: Usuario) -> schemas.UsuarioOut:
    return schemas.UsuarioOut(
        id=u.id, dni=u.dni, nombres=u.nombres, apellidos=u.apellidos,
        email=u.email, telefono=u.telefono, rol=u.rol.nombre.value,
        institucion_id=u.institucion_id, estado=u.estado,
    )

def crear_usuario(db: Session, datos: schemas.UsuarioCreate) -> tuple[Usuario, str]:
    if db.query(Usuario).filter(Usuario.dni == datos.dni).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe un usuario con ese DNI")
    if datos.email and db.query(Usuario).filter(Usuario.email == datos.email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe un usuario con ese correo")
    if datos.institucion_id and not db.get(Institucion, datos.institucion_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Institución no encontrada")
    if datos.rol != RolNombre.super_admin and not datos.institucion_id:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Este rol debe pertenecer a una institución")

    rol = db.query(Rol).filter(Rol.nombre == datos.rol).first()
    if not rol:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "El rol no está registrado en el sistema")

    password = generar_password()
    usuario = Usuario(
        dni=datos.dni, nombres=datos.nombres, apellidos=datos.apellidos,
        email=datos.email, telefono=datos.telefono, rol_id=rol.id,
        institucion_id=datos.institucion_id, password_hash=hash_password(password),
    )
    db.add(usuario)
    db.flush()
    if datos.rol == RolNombre.docente:
        db.add(Docente(id=usuario.id, especialidad=datos.especialidad))
    db.commit()
    db.refresh(usuario)
    return usuario, password

def listar_usuarios(db: Session, institucion_id: Optional[UUID] = None, rol: Optional[RolNombre] = None) -> list[Usuario]:
    q = db.query(Usuario).join(Rol, Rol.id == Usuario.rol_id)
    if institucion_id:
        q = q.filter(Usuario.institucion_id == institucion_id)
    if rol:
        q = q.filter(Rol.nombre == rol)
    return q.order_by(Usuario.apellidos, Usuario.nombres).all()

def obtener_usuario(db: Session, usuario_id: UUID) -> Usuario:
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
    return usuario

def actualizar_usuario(db: Session, usuario_id: UUID, datos: schemas.UsuarioUpdate) -> Usuario:
    usuario = obtener_usuario(db, usuario_id)
    cambios = datos.model_dump(exclude_unset=True)
    nuevo_email = cambios.get("email")
    if nuevo_email and db.query(Usuario).filter(Usuario.email == nuevo_email, Usuario.id != usuario.id).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe un usuario con ese correo")
    if "especialidad" in cambios:
        especialidad = cambios.pop("especialidad")
        if usuario.docente:
            usuario.docente.especialidad = especialidad
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario

def restablecer_password(db: Session, usuario_id: UUID) -> str:
    usuario = obtener_usuario(db, usuario_id)
    password = generar_password()
    usuario.password_hash = hash_password(password)
    db.commit()
    return password