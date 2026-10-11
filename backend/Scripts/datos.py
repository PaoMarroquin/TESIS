"""
Crea datos mínimos de prueba para poder probar RF05 (carga de Excel)
sin tener que construir todavía el CRUD real de RF02:

    docker compose exec backend python -m scripts.crear_datos_prueba

Requiere haber corrido antes scripts.seed_curricular (necesita los
roles ya creados). Es idempotente: si ya corriste esto antes, no
duplica nada, solo te muestra los IDs que ya existen.
"""
from datetime import date

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.academico import Aula, Estudiante, Matricula
from app.models.enums import EstadoMatricula, Gestion, RolNombre, TipoDocumento
from app.models.institucion import AnioAcademico, Docente, Institucion, Rol, Usuario

ESTUDIANTES_PRUEBA = [
    ("Ana", "Torres Quispe"),
    ("Bruno", "Salazar Lima"),
    ("Camila", "Huamán Rojas"),
    ("Diego", "Mendoza Vega"),
    ("Elena", "Castillo Paredes"),
]


def run():
    db = SessionLocal()
    try:
        # --- Institución ---
        institucion = db.query(Institucion).filter_by(codigo_modular="0123456").first()
        if not institucion:
            institucion = Institucion(
                nombre="I.E. 1234 San Martín (prueba)",
                codigo_modular="0123456",
                gestion=Gestion.publica,
                ugel="UGEL 03 Lima",
                dre="DRE Lima Metropolitana",
            )
            db.add(institucion)
            db.flush()
        print(f"institucion_id: {institucion.id}")

        # --- Año académico ---
        anio = (
            db.query(AnioAcademico)
            .filter_by(institucion_id=institucion.id, anio=2026)
            .first()
        )
        if not anio:
            anio = AnioAcademico(
                institucion_id=institucion.id,
                anio=2026,
                fecha_inicio=date(2026, 3, 1),
                fecha_fin=date(2026, 12, 15),
                estado="activo",
            )
            db.add(anio)
            db.flush()
        print(f"anio_academico_id: {anio.id}")

        # --- Usuario + Docente ---
        rol_docente = db.query(Rol).filter_by(nombre=RolNombre.docente).first()
        if not rol_docente:
            print("Falta el rol 'docente'. Corre primero scripts.seed_curricular")
            return

        usuario_docente = db.query(Usuario).filter_by(email="docente@prueba.com").first()
        if not usuario_docente:
            usuario_docente = Usuario(
                institucion_id=institucion.id,
                rol_id=rol_docente.id,
                nombres="Rosa",
                apellidos="Fernández Díaz",
                email="docente@prueba.com",
                password_hash=hash_password("docente123"),
            )
            db.add(usuario_docente)
            db.flush()

            docente = Docente(id=usuario_docente.id, especialidad="Comunicación")
            db.add(docente)
            db.flush()
        else:
            docente = db.query(Docente).filter_by(id=usuario_docente.id).first()
        print(f"docente_id (= usuario_id): {docente.id}  (login: docente@prueba.com / docente123)")

        # --- Aula ---
        aula = (
            db.query(Aula)
            .filter_by(anio_academico_id=anio.id, grado=3, seccion="A")
            .first()
        )
        if not aula:
            aula = Aula(
                institucion_id=institucion.id,
                anio_academico_id=anio.id,
                docente_id=docente.id,
                grado=3,
                seccion="A",
            )
            db.add(aula)
            db.flush()
        print(f"aula_id: {aula.id}  (3° A)")

        # --- Estudiantes + Matrícula ---
        for i, (nombres, apellidos) in enumerate(ESTUDIANTES_PRUEBA, start=1):
            numero_doc = f"7000000{i}"
            estudiante = (
                db.query(Estudiante)
                .filter_by(tipo_documento=TipoDocumento.DNI, numero_documento=numero_doc)
                .first()
            )
            if not estudiante:
                estudiante = Estudiante(
                    institucion_id=institucion.id,
                    tipo_documento=TipoDocumento.DNI,
                    numero_documento=numero_doc,
                    nombres=nombres,
                    apellidos=apellidos,
                )
                db.add(estudiante)
                db.flush()

            matricula_existente = (
                db.query(Matricula)
                .filter_by(estudiante_id=estudiante.id, anio_academico_id=anio.id)
                .first()
            )
            if not matricula_existente:
                db.add(
                    Matricula(
                        estudiante_id=estudiante.id,
                        aula_id=aula.id,
                        anio_academico_id=anio.id,
                        fecha_matricula=date(2026, 3, 1),
                        estado=EstadoMatricula.activo,
                    )
                )

        db.commit()

        total_estudiantes = (
            db.query(Matricula).filter_by(aula_id=aula.id).count()
        )
        print(f"Estudiantes matriculados en el aula: {total_estudiantes} (esperado: {len(ESTUDIANTES_PRUEBA)})")
        print("Listo. Ya puedes usar aula_id y docente_id de arriba para probar RF05.")
    finally:
        db.close()


if __name__ == "__main__":
    run()