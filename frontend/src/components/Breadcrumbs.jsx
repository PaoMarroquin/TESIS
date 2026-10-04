import { Link } from "react-router-dom";

export default function Breadcrumbs({ items }) {
  return (
    <nav className="mb-2 text-sm text-slate-500">
      {items.map((it, i) => (
        <span key={i}>
          {it.to ? (
            <Link to={it.to} className="text-blue-700 hover:underline">
              {it.label}
            </Link>
          ) : (
            <strong className="text-slate-800">{it.label}</strong>
          )}
          {i < items.length - 1 && " / "}
        </span>
      ))}
    </nav>
  );
}