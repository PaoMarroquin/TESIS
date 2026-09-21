from datetime import date, datetime
from typing import Optional
from uuid import UUID as PyUUID

from sqlalchemy import Date, Enum, ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin
from app.models.enums import EstadoGeneral, Gestion, RolNombre

from typing import TYPE_CHECKING, Optional 
if TYPE_CHECKING:
    from app.models.academico import Aula

class Institucion(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "institucion"
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    codigo_modular: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    gestion: Mapped[Gestion] = mapped_column(Enum(Gestion, name="enum_gestion"), nullable=False)
    ugel: Mapped[Optional[str]] = mapped_column(String(150))
    dre: Mapped[Optional[str]] = mapped_column(String(150))
    direccion: Mapped[Optional[str]] = mapped_column(String(255))
    logo_url: Mapped[Optional[str]] = mapped_column(String)
    color_primario: Mapped[Optional[str]] = mapped_column(String(7))
    color_secundario: Mapped[Optional[str]] = mapped_column(String(7))
    estado: Mapped[EstadoGeneral] = mapped_column(Enum(EstadoGeneral, name="enum_estado_general"),default=EstadoGeneral.activo,nullable=False,)
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="institucion")
    anios_academicos: Mapped[list["AnioAcademico"]] = relationship(back_populates="institucion")
    configuraciones: Mapped[list["ConfiguracionInstitucion"]] = relationship(back_populates="institucion")

class Rol(Base):
    __tablename__ = "rol"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[RolNombre] = mapped_column(Enum(RolNombre, name="enum_rol"), unique=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String)
    permisos: Mapped[Optional[dict]] = mapped_column(JSONB)
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="rol")

class Usuario(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "usuario"
    institucion_id: Mapped[Optional[PyUUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("institucion.id"), nullable=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("rol.id"), nullable=False)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    estado: Mapped[EstadoGeneral] = mapped_column(Enum(EstadoGeneral, name="enum_estado_general"),default=EstadoGeneral.activo,nullable=False,)
    ultimo_acceso: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    institucion: Mapped[Optional["Institucion"]] = relationship(back_populates="usuarios")
    rol: Mapped["Rol"] = relationship(back_populates="usuarios")
    docente: Mapped[Optional["Docente"]] = relationship(back_populates="usuario", uselist=False)

class Docente(Base):
    __tablename__ = "docente"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuario.id"), primary_key=True)
    especialidad: Mapped[Optional[str]] = mapped_column(String(100))
    codigo_docente: Mapped[Optional[str]] = mapped_column(String(30))
    usuario: Mapped["Usuario"] = relationship(back_populates="docente")
    aulas: Mapped[list["Aula"]] = relationship(back_populates="docente")

class ConfiguracionInstitucion(UUIDPKMixin, Base):
    __tablename__ = "configuracion_institucion"
    __table_args__ = (UniqueConstraint("institucion_id", "clave"),)
    institucion_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institucion.id"), nullable=False)
    clave: Mapped[str] = mapped_column(String(100), nullable=False)
    valor: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String)
    institucion: Mapped["Institucion"] = relationship(back_populates="configuraciones")

class AnioAcademico(UUIDPKMixin, Base):
    __tablename__ = "anio_academico"
    __table_args__ = (UniqueConstraint("institucion_id", "anio"),)

    institucion_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institucion.id"), nullable=False)
    anio: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo", nullable=False)
    institucion: Mapped["Institucion"] = relationship(back_populates="anios_academicos")
    aulas: Mapped[list["Aula"]] = relationship(back_populates="anio_academico")