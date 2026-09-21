"""habilitar extensiones pgcrypto y vector

Revision ID: 0001
Revises:
Create Date: 2026-09-13

Esta migración va primero y a mano (no la genera autogenerate):
- pgcrypto -> permite gen_random_uuid() para las PK tipo UUID
- vector   -> tipo VECTOR de pgvector, usado en fragmento_curricular
En Supabase normalmente ya vienen habilitadas, pero se deja explícito
para que el proyecto funcione igual en cualquier Postgres limpio.
"""
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    # No se eliminan las extensiones en el downgrade: podrían estar en
    # uso por otros esquemas/servicios dentro del mismo proyecto Supabase.
    pass
