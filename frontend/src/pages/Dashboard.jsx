import { Link } from "react-router-dom";
import { Plus } from "lucide-react";

// TODO: reemplazar por GET /aulas cuando exista el endpoint
const aulas = [
  { id: 1, grado: "3°", seccion: "A", estudiantes: 28 },
  { id: 2, grado: "3°", seccion: "B", estudiantes: 26 },
  { id: 3, grado: "4°", seccion: "A", estudiantes: 30 },
];

export default function Dashboard() {
  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800">Mis aulas</h2>
      <p className="mb-5 text-slate-600">Elige el aula con la que quieres trabajar.</p>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {aulas.map((a) => (
          <Link
            key={a.id}
            to={`/aulas/${a.id}`}
            className="flex flex-col gap-1 rounded-2xl bg-white p-6 shadow transition hover:shadow-lg"
          >
            <span className="text-3xl font-bold text-blue-900">
              {a.grado} "{a.seccion}"
            </span>
            <span className="text-slate-700">Comunicación</span>
            <span className="text-sm text-slate-500">{a.estudiantes} estudiantes</span>
          </Link>
        ))}

        <button className="flex flex-col items-center justify-center gap-2 rounded-2xl border-2 border-dashed border-slate-400 p-6 text-slate-600 hover:bg-white">
          <Plus /> Crear nueva aula
        </button>
      </div>
    </>
  );
}