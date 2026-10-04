import { Outlet, Link } from "react-router-dom";
import { Home, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { user, logout } = useAuth();
  const ie = user?.institucion;
  const anio = new Date().getFullYear();

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="bg-blue-900 text-white">
        <div className="mx-auto max-w-5xl px-4 py-3 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <Link to="/" className="text-lg font-bold">
            Fichas de Evaluación
          </Link>

          <div className="text-sm md:text-center">
            <p className="font-semibold">{ie?.nombre ?? "I.E. sin asignar"}</p>
            <p className="text-blue-200">
              {ie?.nivel ?? "Primaria"} · UGEL {ie?.ugel ?? "—"} · Año lectivo {anio}
            </p>
          </div>

          <div className="flex items-center gap-3 text-sm">
            <span className="hidden sm:inline">{user?.nombre}</span>
            <Link
              to="/"
              className="flex items-center gap-1 rounded-lg bg-blue-800 px-3 py-1.5 hover:bg-blue-700"
            >
              <Home size={16} /> Inicio
            </Link>
            <button
              onClick={logout}
              className="flex items-center gap-1 rounded-lg bg-blue-800 px-3 py-1.5 hover:bg-blue-700"
            >
              <LogOut size={16} /> Cerrar sesión
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
}