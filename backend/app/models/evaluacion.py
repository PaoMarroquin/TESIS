from typing import Optional
from uuid import UUID as PyUUID

from sqlalchemy import (Boolean,CheckConstraint,Enum,ForeignKey,Integer,Numeric,SmallInteger,String,UniqueConstraint,)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin
from app.models.enums import (EstadoArchivoCarga,NivelLogro,SeveridadAlerta,Tendencia,TipoAlerta,)

class RegistroAuxiliarCarga(UUIDPKMixin, Base):
    __tablename__ = "registro_auxiliar_carga"
    __table_args__ = (CheckConstraint("numero_periodo BETWEEN 1 AND 4", name="numero_periodo_valido"),)
    aula_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("aula.id"), nullable=False)
    docente_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("docente.id"), nullable=False)
    anio_academico_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("anio_academico.id"), nullable=False)
    numero_periodo: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False)
    url_archivo_storage: Mapped[Optional[str]] = mapped_column(String)
    estado: Mapped[EstadoArchivoCarga] = mapped_column(Enum(EstadoArchivoCarga, name="enum_estado_archivo"),default=EstadoArchivoCarga.pendiente,nullable=False,)
    incluye_comentarios: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    log_errores: Mapped[Optional[dict]] = mapped_column(JSONB)
    filas_procesadas: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

class Evaluacion(Base):
    __tablename__ = "evaluacion"
    __table_args__ = (UniqueConstraint("matricula_id", "capacidad_id", "numero_periodo"),CheckConstraint("nivel_logro_numerico BETWEEN 1 AND 4", name="nivel_logro_numerico_valido"),)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    matricula_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("matricula.id"), nullable=False)
    capacidad_id: Mapped[int] = mapped_column(ForeignKey("capacidad.id"), nullable=False)
    registro_auxiliar_carga_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("registro_auxiliar_carga.id"), nullable=False)
    numero_periodo: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    nivel_logro_literal: Mapped[NivelLogro] = mapped_column(Enum(NivelLogro, name="enum_nivel_logro"), nullable=False)
    nivel_logro_numerico: Mapped[int] = mapped_column(SmallInteger, nullable=False)

class Asistencia(Base):
    __tablename__ = "asistencia"
    __table_args__ = (UniqueConstraint("matricula_id", "numero_periodo"),)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    matricula_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("matricula.id"), nullable=False)
    registro_auxiliar_carga_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("registro_auxiliar_carga.id"), nullable=False)
    numero_periodo: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    dias_habiles: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    dias_asistidos: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    dias_falta: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    porcentaje_asistencia: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

class AnalisisAcademico(UUIDPKMixin, Base):
    __tablename__ = "analisis_academico"
    __table_args__ = (UniqueConstraint("matricula_id", "competencia_id", "numero_periodo"),)
    matricula_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("matricula.id"), nullable=False)
    competencia_id: Mapped[int] = mapped_column(ForeignKey("competencia.id"), nullable=False)
    anio_academico_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("anio_academico.id"), nullable=False)
    numero_periodo: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    nivel_promedio_capacidades: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    nivel_consolidado: Mapped[NivelLogro] = mapped_column(Enum(NivelLogro, name="enum_nivel_logro"), nullable=False)
    tendencia: Mapped[Optional[Tendencia]] = mapped_column(Enum(Tendencia, name="enum_tendencia"))

class AlertaAprendizaje(UUIDPKMixin, Base):
    __tablename__ = "alerta_aprendizaje"
    matricula_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("matricula.id"), nullable=False)
    competencia_id: Mapped[Optional[int]] = mapped_column(ForeignKey("competencia.id"))
    tipo: Mapped[TipoAlerta] = mapped_column(Enum(TipoAlerta, name="enum_tipo_alerta"), nullable=False)
    severidad: Mapped[SeveridadAlerta] = mapped_column(Enum(SeveridadAlerta, name="enum_severidad_alerta"), nullable=False)
    numero_periodo: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String)
    estado: Mapped[str] = mapped_column(String(15), default="activa", nullable=False)