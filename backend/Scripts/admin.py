"""
Crea un usuario super_admin de prueba para poder probar el login
mientras no existe el módulo de gestión de usuarios (RF02).

    docker compose exec backend python -m scripts.crear_usuario_prueba
"""
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.enums import RolNombre
from app.models.institucion import Rol, Usuario

EMAIL = "admin@prueba.com"
PASSWORD = "admin123"


def run():
    db = SessionLocal()
    try:
        existente = db.query(Usuario).filter_by(email=EMAIL).first()
        if existente:
            print(f"El usuario {EMAIL} ya existe, no se creó de nuevo.")
            return

        rol_admin = db.query(Rol).filter_by(nombre=RolNombre.super_admin).first()
        if not rol_admin:
            print(
                "No se encontró el rol 'super_admin'. "
                "Corre primero: docker compose exec backend python -m scripts.seed_curricular"
            )
            return

        usuario = Usuario(
            institucion_id=None,
            rol_id=rol_admin.id,
            nombres="Admin",
            apellidos="Prueba",
            email=EMAIL,
            password_hash=hash_password(PASSWORD),
        )
        db.add(usuario)
        db.commit()
        print(f"Usuario de prueba creado -> email: {EMAIL} | password: {PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    run()