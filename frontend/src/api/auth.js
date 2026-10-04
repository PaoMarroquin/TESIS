import client from "./client";

export async function iniciarSesion(dni, password) {
  // FastAPI con OAuth2PasswordRequestForm espera form-urlencoded y el campo "username"
  const data = new URLSearchParams();
  data.append("username", dni);
  data.append("password", password);
  const res = await client.post("/auth/login", data, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return res.data; // { access_token, token_type }
}

export async function obtenerUsuarioActual() {
  const res = await client.get("/auth/me");
  return res.data;
}