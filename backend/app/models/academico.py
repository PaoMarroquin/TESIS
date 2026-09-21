from datetime import date
from typing import Optional
from uuid import UUID as PyUUID

from sqlalchemy import (CheckConstraint,Date,Enum,ForeignKey,SmallInteger,String,UniqueConstraint,)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPKMixin
from app.models.enums import EstadoMatricula, TipoDocumento

from typing import TYPE_CHECKING, Optional 
if TYPE_CHECKING:
    from app.models.institucion import AnioAcademico, Docente

class Aula(UUIDPKMixin, Base):
    __tablename__ = "aula"
    __table_args__ = (UniqueConstraint("anio_academico_id", "grado", "seccion"),CheckConstraint("grado BETWEEN 1 AND 6", name="grado_valido"),)

    institucion_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institucion.id"), nullable=False)
    anio_academico_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("anio_academico.id"), nullable=False)
    docente_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("docente.id"), nullable=False)
    grado: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    seccion: Mapped[str] = mapped_column(String(5), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo", nullable=False)
    anio_academico: Mapped["AnioAcademico"] = relationship(back_populates="aulas")
    docente: Mapped["Docente"] = relationship(back_populates="aulas")
    matriculas: Mapped[list["Matricula"]] = relationship(back_populates="aula")

class Estudiante(UUIDPKMixin, Base):
    __tablename__ = "estudiante"
    __table_args__ = (UniqueConstraint("tipo_documento", "numero_documento"),)
    institucion_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("institucion.id"), nullable=False)
    codigo_siagie: Mapped[Optional[str]] = mapped_column(String(20))
    tipo_documento: Mapped[TipoDocumento] = mapped_column(Enum(TipoDocumento, name="enum_tipo_documento"),default=TipoDocumento.DNI,nullable=False,)
    numero_documento: Mapped[Optional[str]] = mapped_column(String(20))
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_nacimiento: Mapped[Optional[date]] = mapped_column(Date)
    sexo: Mapped[Optional[str]] = mapped_column(String(1))
    estado: Mapped[str] = mapped_column(String(20), default="activo", nullable=False)
    matriculas: Mapped[list["Matricula"]] = relationship(back_populates="estudiante")

class Matricula(UUIDPKMixin, Base):
    __tablename__ = "matricula"
    __table_args__ = (UniqueConstraint("estudiante_id", "anio_academico_id"),)
    estudiante_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("estudiante.id"), nullable=False)
    aula_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("aula.id"), nullable=False)
    anio_academico_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("anio_academico.id"), nullable=False)
    fecha_matricula: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[EstadoMatricula] = mapped_column(Enum(EstadoMatricula, name="enum_estado_matricula"),default=EstadoMatricula.activo,nullable=False,)
    estudiante: Mapped["Estudiante"] = relationship(back_populates="matriculas")
    aula: Mapped["Aula"] = relationship(back_populates="matriculas")