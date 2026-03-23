//Name: Craig McMillan
//Student Number: S2390641
//Date: 14/03/26
//This file defines the route structure for the application

import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AnalysisPage from "./pages/AnalysisPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/analysis" element={<AnalysisPage />} />
    </Routes>
  );
}
export default App