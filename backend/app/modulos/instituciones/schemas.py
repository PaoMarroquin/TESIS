from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.models.enums import EstadoGeneral, Gestion

COLOR = r"^#[0-9A-Fa-f]{6}$"


class InstitucionCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=200)
    codigo_modular: str = Field(min_length=7, max_length=20)
    gestion: Gestion
    ugel: Optional[str] = Field(None, max_length=150)
    dre: Optional[str] = Field(None, max_length=150)
    direccion: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = None
    color_primario: Optional[str] = Field(None, pattern=COLOR)
    color_secundario: Optional[str] = Field(None, pattern=COLOR)


class InstitucionUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    gestion: Optional[Gestion] = None
    ugel: Optional[str] = Field(None, max_length=150)
    dre: Optional[str] = Field(None, max_length=150)
    direccion: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = None
    color_primario: Optional[str] = Field(None, pattern=COLOR)
    color_secundario: Optional[str] = Field(None, pattern=COLOR)
    estado: Optional[EstadoGeneral] = None


class InstitucionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nombre: str
    codigo_modular: str
    gestion: Gestion
    ugel: Optional[str] = None
    dre: Optional[str] = None
    direccion: Optional[str] = None
    logo_url: Optional[str] = None
    color_primario: Optional[str] = None
    color_secundario: Optional[str] = None
    estado: EstadoGeneral


class AnioAcademicoCreate(BaseModel):
    anio: int = Field(ge=2000, le=2100)
    fecha_inicio: date
    fecha_fin: date

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin <= self.fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la de inicio")
        return self


class AnioAcademicoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    institucion_id: UUID
    anio: int
    fecha_inicio: date
    fecha_fin: date
    estado: str