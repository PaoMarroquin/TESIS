from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.db.session import engine
from app.modulos.auth.router import router as auth_router

app = FastAPI(title="Sistema de Fichas de Evaluación")

# --- CORS ---
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers de cada módulo (monolito modular) ---
app.include_router(auth_router)

@app.get("/")
def home():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"mensaje": "Conexión exitosa con PostgreSQL"}
