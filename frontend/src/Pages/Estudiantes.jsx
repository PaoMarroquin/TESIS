import { useEffect, useState } from "react";

function Estudiantes() {

  const [archivoExcel, setArchivoExcel] = useState(null);

  const [grado, setGrado] = useState("6");

  const [seccion, setSeccion] = useState("A");

  const [estudiantes, setEstudiantes] = useState([]);

  const [editandoId, setEditandoId] = useState(null);

  const [nombresEdit, setNombresEdit] = useState("");

  const [apellidosEdit, setApellidosEdit] = useState("");

  const [gradoEdit, setGradoEdit] = useState("");

  const [seccionEdit, setSeccionEdit] = useState("");

  const cargarEstudiantes = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/students"
      );

      const data = await response.json();

      setEstudiantes(data);

    } catch (error) {

      console.error(error);

    }

  };

  useEffect(() => {

    cargarEstudiantes();

  }, []);

  const importarEstudiantes = async () => {

    if (!archivoExcel) {

      alert("Seleccione un Excel");

      return;

    }

    const formData = new FormData();

    formData.append("file", archivoExcel);

    formData.append("grado", grado);

    formData.append("seccion", seccion);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/students/upload",
        {
          method: "POST",
          body: formData
        }
      );

      const resultado = await response.json();

      alert(resultado.mensaje);

      await cargarEstudiantes();

    } catch (error) {

      console.error(error);

      alert("Error al importar estudiantes");

    }

  };

  const eliminarEstudiante = async (id) => {

    const confirmar = window.confirm(
      "¿Desea eliminar este estudiante?"
    );

    if (!confirmar) return;

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/students/${id}`,
        {
          method: "DELETE"
        }
      );

      const resultado = await response.json();

      alert(resultado.mensaje);

      await cargarEstudiantes();

    } catch (error) {

      console.error(error);

    }

  };

  const iniciarEdicion = (estudiante) => {

    setEditandoId(estudiante.id);

    setNombresEdit(estudiante.nombres);

    setApellidosEdit(estudiante.apellidos);

    setGradoEdit(estudiante.grado);

    setSeccionEdit(estudiante.seccion);

  };

  const guardarEdicion = async () => {

    const formData = new FormData();

    formData.append("nombres", nombresEdit);

    formData.append("apellidos", apellidosEdit);

    formData.append("grado", gradoEdit);

    formData.append("seccion", seccionEdit);

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/students/${editandoId}`,
        {
          method: "PUT",
          body: formData
        }
      );

      const resultado = await response.json();

      alert(resultado.mensaje);

      setEditandoId(null);

      await cargarEstudiantes();

    } catch (error) {

      console.error(error);

    }

  };

  return (

    <div>

      <h2>Estudiantes</h2>

      <div style={{ marginBottom: "20px" }}>

        <label>Grado:</label>

        <select
          value={grado}
          onChange={(e) =>
            setGrado(e.target.value)
          }
        >
          <option value="1">1°</option>
          <option value="2">2°</option>
          <option value="3">3°</option>
          <option value="4">4°</option>
          <option value="5">5°</option>
          <option value="6">6°</option>
        </select>

        <label
          style={{
            marginLeft: "15px"
          }}
        >
          Sección:
        </label>

        <select
          value={seccion}
          onChange={(e) =>
            setSeccion(e.target.value)
          }
        >
          <option value="A">A</option>
          <option value="B">B</option>
          <option value="C">C</option>
        </select>

        <br />
        <br />

        <input
          type="file"
          accept=".xlsx,.xls"
          onChange={(e) =>
            setArchivoExcel(
              e.target.files[0]
            )
          }
        />

        <button
          onClick={importarEstudiantes}
          style={{
            marginLeft: "10px"
          }}
        >
          Importar Excel
        </button>

      </div>

      <table
        border="1"
        cellPadding="8"
      >

        <thead>

          <tr>

            <th>ID</th>
            <th>Nombres</th>
            <th>Apellidos</th>
            <th>Grado</th>
            <th>Sección</th>
            <th>Acciones</th>

          </tr>

        </thead>

        <tbody>

          {estudiantes.map(
            (estudiante) => (

              <tr key={estudiante.id}>

                <td>
                  {estudiante.id}
                </td>

                <td>

                  {editandoId === estudiante.id ? (

                    <input
                      value={nombresEdit}
                      onChange={(e) =>
                        setNombresEdit(
                          e.target.value
                        )
                      }
                    />

                  ) : (

                    estudiante.nombres

                  )}

                </td>

                <td>

                  {editandoId === estudiante.id ? (

                    <input
                      value={apellidosEdit}
                      onChange={(e) =>
                        setApellidosEdit(
                          e.target.value
                        )
                      }
                    />

                  ) : (

                    estudiante.apellidos

                  )}

                </td>

                <td>

                  {editandoId === estudiante.id ? (

                    <input
                      value={gradoEdit}
                      onChange={(e) =>
                        setGradoEdit(
                          e.target.value
                        )
                      }
                    />

                  ) : (

                    estudiante.grado

                  )}

                </td>

                <td>

                  {editandoId === estudiante.id ? (

                    <input
                      value={seccionEdit}
                      onChange={(e) =>
                        setSeccionEdit(
                          e.target.value
                        )
                      }
                    />

                  ) : (

                    estudiante.seccion

                  )}

                </td>

                <td>

                  {editandoId === estudiante.id ? (

                    <button
                      onClick={
                        guardarEdicion
                      }
                    >
                      Guardar
                    </button>

                  ) : (

                    <button
                      onClick={() =>
                        iniciarEdicion(
                          estudiante
                        )
                      }
                    >
                      Editar
                    </button>

                  )}

                  <button
                    style={{
                      marginLeft: "5px"
                    }}
                    onClick={() =>
                      eliminarEstudiante(
                        estudiante.id
                      )
                    }
                  >
                    Eliminar
                  </button>

                </td>

              </tr>

            )
          )}

        </tbody>

      </table>

    </div>

  );

}

export default Estudiantes;