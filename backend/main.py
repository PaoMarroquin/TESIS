from fastapi import FastAPI, UploadFile,HTTPException, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import shutil
import re

from sqlalchemy import text
from backend.app.db.session import engine


app = FastAPI()

# CORS
origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {
        "mensaje": "Conexión exitosa con PostgreSQL"
    }


# =====================================================
# DOCUMENTOS CURRICULARES
# =====================================================

@app.get("/curricular-documents")
def get_curricular_documents():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    nombre,
                    tipo_documento,
                    version,
                    fecha_subida,
                    estado_vectorizacion
                FROM documentos_curriculares
                ORDER BY id DESC
            """)
        )

        documentos = []

        for row in result:

            documentos.append({
                "id": row.id,
                "nombre": row.nombre,
                "tipo_documento": row.tipo_documento,
                "version": row.version,
                "fecha_subida": str(row.fecha_subida),
                "estado_vectorizacion": row.estado_vectorizacion
            })

        return documentos


@app.post("/curricular-documents")
async def upload_curricular_document(
    file: UploadFile = File(...)
):

    storage_path = "storage/curriculum"

    os.makedirs(storage_path, exist_ok=True)

    file_path = os.path.join(
        storage_path,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with engine.connect() as conn:

        conn.execute(
            text("""
                INSERT INTO documentos_curriculares
                (
                    nombre,
                    tipo_documento,
                    version,
                    ruta_archivo,
                    estado_vectorizacion
                )
                VALUES
                (
                    :nombre,
                    'Curricular',
                    '1.0',
                    :ruta,
                    false
                )
            """),
            {
                "nombre": file.filename,
                "ruta": file_path
            }
        )

        conn.commit()

    return {
        "mensaje": "Documento guardado correctamente"
    }


@app.delete("/curricular-documents/{document_id}")
def delete_curricular_document(document_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT ruta_archivo
                FROM documentos_curriculares
                WHERE id = :id
            """),
            {"id": document_id}
        )

        documento = result.fetchone()

        if documento is None:

            return {
                "mensaje": "Documento no encontrado"
            }

        ruta_archivo = documento.ruta_archivo

        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

        conn.execute(
            text("""
                DELETE FROM documentos_curriculares
                WHERE id = :id
            """),
            {"id": document_id}
        )

        conn.commit()

    return {
        "mensaje": "Documento eliminado correctamente"
    }


# =====================================================
# ESTUDIANTES
# =====================================================

@app.get("/students")
def get_students():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    codigo,
                    nombres,
                    apellidos,
                    grado,
                    seccion,
                    fecha_registro
                FROM estudiantes
                ORDER BY apellidos, nombres
            """)
        )

        estudiantes = []

        for row in result:

            estudiantes.append({
                "id": row.id,
                "codigo": row.codigo,
                "nombres": row.nombres,
                "apellidos": row.apellidos,
                "grado": row.grado,
                "seccion": row.seccion,
                "fecha_registro": str(row.fecha_registro)
            })

        return estudiantes


@app.post("/students/upload")
async def upload_students(
    file: UploadFile = File(...),
    grado: str = Form(...),
    seccion: str = Form(...)
):

    try:

        df = pd.read_excel(
            file.file,
            engine="openpyxl"
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Excel inválido"
        )

    registros_insertados = 0

    with engine.connect() as conn:

        for _, row in df.iterrows():

            codigo = str(
                row.get("CODIGO", "")
            ).strip()

            nombres = str(
                row.get("NOMBRES", "")
            ).strip()

            apellidos = str(
                row.get("APELLIDOS", "")
            ).strip()

            if nombres == "":
                continue

            apellidos = apellidos.replace(",", "")

            existe = conn.execute(
                text("""
                    SELECT id
                    FROM estudiantes
                    WHERE nombres = :nombres
                    AND apellidos = :apellidos
                    AND grado = :grado
                    AND seccion = :seccion
                """),
                {
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "grado": grado,
                    "seccion": seccion
                }
            ).fetchone()

            if existe:
                continue

            conn.execute(
                text("""
                    INSERT INTO estudiantes
                    (
                        codigo,
                        nombres,
                        apellidos,
                        grado,
                        seccion
                    )
                    VALUES
                    (
                        :codigo,
                        :nombres,
                        :apellidos,
                        :grado,
                        :seccion
                    )
                """),
                {
                    "codigo": codigo,
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "grado": grado,
                    "seccion": seccion
                }
            )

            registros_insertados += 1

        conn.commit()

    return {
        "mensaje": f"{registros_insertados} estudiantes importados"
    }

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    nombres: str = Form(...),
    apellidos: str = Form(...),
    grado: str = Form(...),
    seccion: str = Form(...)
):

    with engine.connect() as conn:

        conn.execute(
            text("""
                UPDATE estudiantes
                SET
                    nombres = :nombres,
                    apellidos = :apellidos,
                    grado = :grado,
                    seccion = :seccion
                WHERE id = :id
            """),
            {
                "id": student_id,
                "nombres": nombres,
                "apellidos": apellidos,
                "grado": grado,
                "seccion": seccion
            }
        )

        conn.commit()

    return {
        "mensaje": "Estudiante actualizado"
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    with engine.connect() as conn:

        conn.execute(
            text("""
                DELETE FROM estudiantes
                WHERE id = :id
            """),
            {
                "id": student_id
            }
        )

        conn.commit()

    return {
        "mensaje": "Estudiante eliminado"
    }