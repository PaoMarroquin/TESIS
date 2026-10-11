import re
from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import verify_password
from app.models.enums import EstadoGeneral
from app.models.institucion import Usuario

DNI_RE = re.compile(r"^\d{8}$")

def authenticate_user(db: Session, identificador: str, password: str) -> Optional[Usuario]:
    identificador = identificador.strip()
    campo = Usuario.dni if DNI_RE.match(identificador) else Usuario.email
    usuario = db.query(Usuario).filter(campo == identificador).first()

    if not usuario or not usuario.password_hash:
        return None
    if usuario.estado != EstadoGeneral.activo:
        return None
    if not verify_password(password, usuario.password_hash):
        return None
    return usuario