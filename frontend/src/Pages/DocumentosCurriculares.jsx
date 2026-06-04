import { useEffect, useState } from "react";

function DocumentosCurriculares() {

  const [archivo, setArchivo] = useState(null);
  const [documentos, setDocumentos] = useState([]);

  const cargarDocumentos = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/curricular-documents"
      );

      const data = await response.json();

      setDocumentos(data);

    } catch (error) {

      console.error(error);

    }

  };

  useEffect(() => {

    cargarDocumentos();

  }, []);

  const subirArchivo = async () => {

    if (!archivo) {

      alert("Seleccione un PDF");

      return;

    }

    const formData = new FormData();

    formData.append("file", archivo);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/curricular-documents",
        {
          method: "POST",
          body: formData,
        }
      );

      const resultado = await response.json();

      alert(resultado.mensaje);

      await cargarDocumentos();

    } catch (error) {

      console.error(error);

    }

  };

  const eliminarDocumento = async (id) => {

    const confirmar = window.confirm(
      "¿Desea eliminar este documento?"
    );

    if (!confirmar) return;

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/curricular-documents/${id}`,
        {
          method: "DELETE"
        }
      );

      const resultado = await response.json();

      alert(resultado.mensaje);

      await cargarDocumentos();

    } catch (error) {

      console.error(error);

    }

  };

  return (

    <div>

      <h2>Documentos Curriculares</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setArchivo(e.target.files[0])
        }
      />

      <button
        onClick={subirArchivo}
        style={{ marginLeft: "10px" }}
      >
        Subir PDF
      </button>

      <br /><br />

      <table border="1" cellPadding="8">

        <thead>

          <tr>

            <th>ID</th>
            <th>Documento</th>
            <th>Tipo</th>
            <th>Versión</th>
            <th>Fecha</th>
            <th>Estado</th>
            <th>Acción</th>

          </tr>

        </thead>

        <tbody>

          {documentos.map((doc) => (

            <tr key={doc.id}>

              <td>{doc.id}</td>

              <td>{doc.nombre}</td>

              <td>{doc.tipo_documento}</td>

              <td>{doc.version}</td>

              <td>{doc.fecha_subida}</td>

              <td>
                {doc.estado_vectorizacion
                  ? "Vectorizado"
                  : "Pendiente"}
              </td>

              <td>

                <button
                  onClick={() =>
                    eliminarDocumento(doc.id)
                  }
                >
                  Eliminar
                </button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

}

export default DocumentosCurriculares;