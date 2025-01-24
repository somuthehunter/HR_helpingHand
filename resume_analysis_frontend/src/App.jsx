import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import ButtonGradient from "./assets/svg/ButtonGradient";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Benefits from "./components/Benefits";
import Collaboration from "./components/Collaboration";
import Services from "./components/Services";
import Pricing from "./components/Pricing";
import Roadmap from "./components/Roadmap";
import Footer from "./components/Footer";
import LoginModal from "./components/LoginModal";
import SignUpModal from "./components/SignupModal";
import Dashboard from "./components/hr_side_dashboard/Dashboard";

const App = () => {
  const location = useLocation();
  const hideHeaderRoutes = ["/dashboard"]; // Routes where Header should be hidden

  return (
    <div className="pt-[4.75] lg:pt-[5.25] overflow-hidden">
      {/* Hide Header on specific routes */}
      {!hideHeaderRoutes.includes(location.pathname) && <Header />}

      <Routes>
        <Route 
          path="/" 
          element={
            <>
              <Hero />
              <Benefits />
              <Collaboration />
              <Services />
              <Pricing />
              <Roadmap />
              <Footer />
            </>
          } 
        />
        <Route path="/login" element={<LoginModal />} />
        <Route path="/register" element={<SignUpModal />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>

      {/* Hide ButtonGradient on dashboard */}
      {!hideHeaderRoutes.includes(location.pathname) && <ButtonGradient />}
    </div>
  );
};

export default App;
