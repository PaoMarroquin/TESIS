import { useParams, Link } from "react-router-dom";
import { Users, ClipboardCheck, BookOpen, ArrowLeft } from "lucide-react";
import Breadcrumbs from "../components/Breadcrumbs";

export default function AulaDetalle() {
  const { aulaId } = useParams();

  const opciones = [
    { Icono: Users, titulo: "Ver a mis estudiantes", to: `/aulas/${aulaId}/estudiantes` },
    { Icono: ClipboardCheck, titulo: "Evaluar y ver mis reportes", to: `/aulas/${aulaId}/evaluaciones` },
    { Icono: BookOpen, titulo: "Recursos pedagógicos", to: `/aulas/${aulaId}/recursos` },
  ];

  return (
    <>
      <Breadcrumbs items={[{ label: "Mis aulas", to: "/" }, { label: `Aula ${aulaId}` }]} />

      <Link
        to="/"
        className="mb-4 inline-flex items-center gap-1 font-medium text-blue-700 hover:underline"
      >
        <ArrowLeft size={16} /> Regresar a Mis aulas
      </Link>

      <h2 className="mb-5 text-2xl font-bold text-slate-800">
        ¿Qué quieres hacer en esta aula?
      </h2>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {opciones.map(({ Icono, titulo, to }) => (
          <Link
            key={titulo}
            to={to}
            className="flex flex-col items-center gap-3 rounded-2xl bg-white p-8 text-center shadow transition hover:shadow-lg"
          >
            <Icono size={40} className="text-blue-800" />
            <span className="font-semibold text-slate-800">{titulo}</span>
          </Link>
        ))}
      </div>
    </>
  );
}