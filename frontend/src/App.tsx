import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "@/components/Header";
import Home from "@/pages/home";
import { PATHS } from "@/utils/constant";
import EeIndex from "@/pages/ee-index";
import Download from "@/pages/download";
import Eej from "@/pages/eej";

function App() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-100">
      <Router>
        <Header />
        <Routes>
          <Route path={PATHS.HOME} element={<Home />} />
          <Route path={PATHS.EE_INDEX} element={<EeIndex />} />
          <Route path={PATHS.DOWNLOAD} element={<Download />} />
          <Route path={PATHS.EEJ} element={<Eej />} />
        </Routes>
      </Router>
    </div>
  );
}
export default App;
