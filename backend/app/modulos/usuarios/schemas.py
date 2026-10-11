from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.enums import EstadoGeneral, RolNombre

EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

class UsuarioCreate(BaseModel):
    dni: str = Field(pattern=r"^\d{8}$")
    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    rol: RolNombre
    institucion_id: Optional[UUID] = None
    email: Optional[str] = Field(None, pattern=EMAIL, max_length=150)
    telefono: Optional[str] = Field(None, max_length=20)
    especialidad: Optional[str] = Field(None, max_length=100)  # solo docentes

class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, pattern=EMAIL, max_length=150)
    telefono: Optional[str] = Field(None, max_length=20)
    estado: Optional[EstadoGeneral] = None
    especialidad: Optional[str] = Field(None, max_length=100)

class UsuarioOut(BaseModel):
    id: UUID
    dni: Optional[str] = None
    nombres: str
    apellidos: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    rol: str
    institucion_id: Optional[UUID] = None
    estado: EstadoGeneral

class UsuarioCreado(UsuarioOut):
    password_temporal: str

class PasswordTemporal(BaseModel):
    password_temporal: str