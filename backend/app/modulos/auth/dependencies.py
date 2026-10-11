# Dependencias reutilizables para proteger sus endpoints.
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.institucion import Usuario
from app.models.enums import EstadoGeneral


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = decode_access_token(token)
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    usuario = db.query(Usuario).filter(Usuario.id == UUID(usuario_id)).first()
    if usuario is None:
        raise credentials_exception
    if usuario is None or usuario.estado != EstadoGeneral.activo:
        raise credentials_exception
    return usuario

def require_roles(*roles_permitidos):
    permitidos = {getattr(r, "value", r) for r in roles_permitidos}

    def verificador(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        if usuario.rol.nombre.value not in permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción",
            )
        return usuario

    return verificador