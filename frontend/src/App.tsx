import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Sidebar } from "./components/shared";
import { useAuthStore } from "./store/auth";
import LoginPage from "./pages/Login";
import RFPPage from "./pages/RFP";
import FleetPage from "./pages/Fleet";
import ConstructionPage from "./pages/Construction";
import FranchisePage from "./pages/Franchise";
import SolarPage from "./pages/Solar";
import HospitalityPage from "./pages/Hospitality";
import VenuePage from "./pages/Venue";
import SourcingPage from "./pages/Sourcing";
import AgencyPage from "./pages/Agency";
import FoodPage from "./pages/Food";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
    },
  },
});

function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 ml-60 min-h-screen overflow-y-auto">
        {children}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<Navigate to="/rfp" replace />} />
          <Route path="/rfp" element={<ProtectedLayout><RFPPage /></ProtectedLayout>} />
          <Route path="/fleet" element={<ProtectedLayout><FleetPage /></ProtectedLayout>} />
          <Route path="/construction" element={<ProtectedLayout><ConstructionPage /></ProtectedLayout>} />
          <Route path="/franchise" element={<ProtectedLayout><FranchisePage /></ProtectedLayout>} />
          <Route path="/solar" element={<ProtectedLayout><SolarPage /></ProtectedLayout>} />
          <Route path="/hospitality" element={<ProtectedLayout><HospitalityPage /></ProtectedLayout>} />
          <Route path="/venue" element={<ProtectedLayout><VenuePage /></ProtectedLayout>} />
          <Route path="/sourcing" element={<ProtectedLayout><SourcingPage /></ProtectedLayout>} />
          <Route path="/agency" element={<ProtectedLayout><AgencyPage /></ProtectedLayout>} />
          <Route path="/food" element={<ProtectedLayout><FoodPage /></ProtectedLayout>} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
