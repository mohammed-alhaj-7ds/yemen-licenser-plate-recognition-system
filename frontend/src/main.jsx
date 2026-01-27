import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ToastProvider } from "./components/ToastContainer";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Developers from "./pages/Developers";
import About from "./pages/About";
import UseCases from "./pages/UseCases";
import NotFound from "./pages/NotFound";
import AskAssistant from "./components/AskAssistant";
import "./index.css";

function App() {
  return (
    <BrowserRouter>
      <ToastProvider>
        <div className="app">
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/developers" element={<Developers />} />
              <Route path="/use-cases" element={<UseCases />} />
              <Route path="/about" element={<About />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          <Footer />
          <AskAssistant />
        </div>
      </ToastProvider>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
