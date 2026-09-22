from app.db.session import SessionLocal
from app.models.curricular import Capacidad, Competencia, Curso
from app.models.enums import NivelEducativo, RolNombre
from app.models.institucion import Rol

COMPETENCIAS_Y_CAPACIDADES = [
    {
        "nombre": "Se comunica oralmente en su lengua materna",
        "orden": 1,
        "capacidades": [
            "Obtiene información del texto oral",
            "Infiere e interpreta información del texto oral",
            "Adecúa, organiza y desarrolla las ideas de forma coherente y cohesionada",
            "Utiliza recursos no verbales y paraverbales de forma estratégica",
            "Interactúa estratégicamente con distintos interlocutores",
            "Reflexiona y evalúa la forma, el contenido y contexto del texto oral",
        ],
    },
    {
        "nombre": "Lee diversos tipos de textos escritos en su lengua materna",
        "orden": 2,
        "capacidades": [
            "Obtiene información del texto escrito",
            "Infiere e interpreta información del texto",
            "Reflexiona y evalúa la forma, el contenido y contexto del texto",
        ],
    },
    {
        "nombre": "Escribe diversos tipos de textos en su lengua materna",
        "orden": 3,
        "capacidades": [
            "Adecúa el texto a la situación comunicativa",
            "Organiza y desarrolla las ideas de forma coherente y cohesionada",
            "Utiliza convenciones del lenguaje escrito de forma pertinente",
            "Reflexiona y evalúa la forma, el contenido y contexto del texto escrito",
        ],
    },
]


def run():
    db = SessionLocal()
    try:
        # --- Roles ---
        for rol_nombre in RolNombre:
            existe = db.query(Rol).filter_by(nombre=rol_nombre).first()
            if not existe:
                db.add(Rol(nombre=rol_nombre))

        # --- Curso (Área curricular) ---
        curso = db.query(Curso).filter_by(nombre="Comunicación").first()
        if not curso:
            curso = Curso(nombre="Comunicación", nivel=NivelEducativo.primaria)
            db.add(curso)
            db.flush()  # para obtener curso.id

        # --- Competencias y capacidades ---
        for comp_data in COMPETENCIAS_Y_CAPACIDADES:
            competencia = (
                db.query(Competencia)
                .filter_by(nombre=comp_data["nombre"], curso_id=curso.id)
                .first()
            )
            if not competencia:
                competencia = Competencia(
                    curso_id=curso.id,
                    nombre=comp_data["nombre"],
                    orden=comp_data["orden"],
                )
                db.add(competencia)
                db.flush()

            for i, cap_nombre in enumerate(comp_data["capacidades"], start=1):
                existe_cap = (
                    db.query(Capacidad)
                    .filter_by(nombre=cap_nombre, competencia_id=competencia.id)
                    .first()
                )
                if not existe_cap:
                    db.add(
                        Capacidad(
                            competencia_id=competencia.id,
                            nombre=cap_nombre,
                            orden=i,
                        )
                    )

        db.commit()

        # Resumen de verificación: cuenta lo que quedó realmente en la BD
        total_roles = db.query(Rol).count()
        total_cursos = db.query(Curso).count()
        total_competencias = db.query(Competencia).count()
        total_capacidades = db.query(Capacidad).count()

        print("Seed de catálogos curriculares completado.")
        print(f"  - roles:        {total_roles} (esperado: 3)")
        print(f"  - cursos:       {total_cursos} (esperado: 1)")
        print(f"  - competencias: {total_competencias} (esperado: 3)")
        print(f"  - capacidades:  {total_capacidades} (esperado: 13)")
    finally:
        db.close()


if __name__ == "__main__":
    run()