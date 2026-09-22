from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import verify_password
from app.models.institucion import Usuario

def authenticate_user(db: Session, email: str, password: str) -> Optional[Usuario]:    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not usuario.password_hash:
        return None
    if not verify_password(password, usuario.password_hash):
        return None
    return usuario