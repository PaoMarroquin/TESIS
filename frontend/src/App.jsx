import {
  BrowserRouter,
  Routes,
  Route,
  Link
} from "react-router-dom";

import DocumentosCurriculares from "./pages/DocumentosCurriculares";
import Estudiantes from "./pages/Estudiantes";

function App() {
  return (
    <BrowserRouter>

      <div style={{ padding: "20px" }}>

        <h1>Sistema Borrador inicial</h1>

        <nav>

          <Link to="/">
            Documentos Curriculares
          </Link>

          {" | "}

          <Link to="/students">
            Estudiantes
          </Link>

        </nav>

        <hr />

        <Routes>

          <Route
            path="/"
            element={<DocumentosCurriculares />}
          />

          <Route
            path="/students"
            element={<Estudiantes />}
          />

        </Routes>

      </div>

    </BrowserRouter>
  );
}

export default App;