from typing import Optional
from uuid import UUID as PyUUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import Enum, ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.db.base import Base, TimestampMixin, UUIDPKMixin
from app.models.enums import EstadoDocumentoCurricular, NivelEducativo


class Curso(Base):
    __tablename__ = "curso"
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    nivel: Mapped[NivelEducativo] = mapped_column(Enum(NivelEducativo, name="enum_nivel_educativo"), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String)
    competencias: Mapped[list["Competencia"]] = relationship(back_populates="curso")

class Competencia(Base):
    __tablename__ = "competencia"
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    curso_id: Mapped[int] = mapped_column(ForeignKey("curso.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String)
    orden: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    curso: Mapped["Curso"] = relationship(back_populates="competencias")
    capacidades: Mapped[list["Capacidad"]] = relationship(back_populates="competencia")

class Capacidad(Base):
    __tablename__ = "capacidad"
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    competencia_id: Mapped[int] = mapped_column(ForeignKey("competencia.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String)
    orden: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    competencia: Mapped["Competencia"] = relationship(back_populates="capacidades")

class DocumentoCurricular(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "documento_curricular"
    competencia_id: Mapped[int] = mapped_column(ForeignKey("competencia.id"), nullable=False)
    encargado_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False)
    grado: Mapped[Optional[int]] = mapped_column(SmallInteger)
    url_archivo: Mapped[str] = mapped_column(String, nullable=False)
    estado: Mapped[EstadoDocumentoCurricular] = mapped_column(Enum(EstadoDocumentoCurricular, name="enum_estado_documento"),default=EstadoDocumentoCurricular.activo,nullable=False,)
    fragmentos: Mapped[list["FragmentoCurricular"]] = relationship(back_populates="documento")

class FragmentoCurricular(TimestampMixin, Base):
    __tablename__ = "fragmento_curricular"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    documento_curricular_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documento_curricular.id"), nullable=False)
    contenido_texto: Mapped[str] = mapped_column(String, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(settings.embedding_dim), nullable=False)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB)
    documento: Mapped["DocumentoCurricular"] = relationship(back_populates="fragmentos")