from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class InstitucionResumen(BaseModel):
    id: UUID
    nombre: str
    codigo_modular: str
    ugel: Optional[str] = None
    dre: Optional[str] = None
    anio_lectivo: Optional[int] = None

class UsuarioOut(BaseModel):
    id: UUID
    nombres: str
    apellidos: str
    dni: Optional[str] = None
    email: Optional[str] = None
    rol: str
    institucion_id: Optional[UUID] = None
    institucion: Optional[InstitucionResumen] = None

class CambiarPassword(BaseModel):
    password_actual: str
    password_nueva: str = Field(min_length=8, max_length=72)