from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.bootstrap import asegurar_admin, asegurar_roles
from app.db.session import SessionLocal
from app.modulos.auth.router import router as auth_router
from app.modulos.instituciones.router import router as instituciones_router
from app.modulos.usuarios.router import router as usuarios_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    with SessionLocal() as db:
        asegurar_roles(db)
        asegurar_admin(db)
    yield


app = FastAPI(title="Sistema de Fichas de Evaluación", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(instituciones_router)
app.include_router(usuarios_router)