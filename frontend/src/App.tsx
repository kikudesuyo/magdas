import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Home from "@/pages/Home";
import EeIndexChart from "@/pages/Plot";
import { PATHS } from "@/utils/constant";

function App() {
  return (
    <div className="flex min-h-screen flex-col">
      <Router>
        <Header />
        <Routes>
          <Route path={PATHS.HOME} element={<Home />} />
          <Route path={PATHS.PLOT} element={<EeIndexChart />} />
          <Route path={PATHS.EE_INDEX} element={<EeIndexChart />} />
        </Routes>
        <Footer />
      </Router>
    </div>
  );
}
export default App;
