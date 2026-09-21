from datetime import datetime
from typing import Optional
from uuid import UUID as PyUUID

from sqlalchemy import Enum, ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, UUIDPKMixin
from app.models.enums import EstadoFicha


class FichaEvaluacion(UUIDPKMixin, Base):
    __tablename__ = "ficha_evaluacion"
    __table_args__ = (UniqueConstraint("matricula_id", "numero_periodo"),)
    matricula_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("matricula.id"), nullable=False)
    anio_academico_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("anio_academico.id"), nullable=False)
    numero_periodo: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # antes "bimestre"
    estado: Mapped[EstadoFicha] = mapped_column(Enum(EstadoFicha, name="enum_estado_ficha"),default=EstadoFicha.borrador,nullable=False,)
    observaciones_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    recomendaciones_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    correcciones_docente: Mapped[Optional[dict]] = mapped_column(JSONB)
    validado_por: Mapped[Optional[PyUUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("usuario.id"))
    fecha_validacion: Mapped[Optional[datetime]] = mapped_column()
    url_pdf: Mapped[Optional[str]] = mapped_column(String)
    fecha_exportacion: Mapped[Optional[datetime]] = mapped_column()