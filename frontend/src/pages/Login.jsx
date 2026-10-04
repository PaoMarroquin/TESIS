import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";


export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [dni, setDni] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    if (!/^\d{8}$/.test(dni)) {
      setError("El DNI debe tener 8 dígitos");
      return;
    }
    setSubmitting(true);
    try {
      await login(dni, password);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || "DNI o contraseña incorrectos");
    } finally {
      setSubmitting(false);
    }
  }

  const input =
    "w-full rounded-lg border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-600";

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 p-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm bg-white rounded-2xl shadow p-8 space-y-4"
      >
        <h1 className="text-2xl font-bold text-slate-800">Ingresa a tu cuenta</h1>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">DNI</label>
          <input
            className={input}
            inputMode="numeric"
            maxLength={8}
            placeholder="Ej: 12345678"
            value={dni}
            onChange={(e) => setDni(e.target.value.replace(/\D/g, ""))}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Contraseña</label>
          <input
            className={input}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={submitting}
          className="w-full rounded-lg bg-blue-700 py-2.5 font-semibold text-white hover:bg-blue-800 disabled:opacity-60"
        >
          {submitting ? "Ingresando..." : "Ingresar"}
        </button>
      </form>
    </div>
  );
}