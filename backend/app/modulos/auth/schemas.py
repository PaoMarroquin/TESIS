from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UsuarioOut(BaseModel):
    id: UUID
    nombres: str
    apellidos: str
    email: EmailStr
    rol: str
    institucion_id: Optional[UUID] = None
    model_config = {"from_attributes": True}