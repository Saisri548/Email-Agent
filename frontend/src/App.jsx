import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Emails from "./pages/Emails";
import Invoices from "./pages/Invoices";
import Tasks from "./pages/Tasks";
import Disputes from "./pages/Disputes";
import Audit from "./pages/Audit";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/emails" element={<Emails />} />
        <Route path="/invoices" element={<Invoices />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/disputes" element={<Disputes />} />
        <Route path="/audit" element={<Audit />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;