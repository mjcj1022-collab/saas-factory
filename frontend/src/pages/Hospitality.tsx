import { PageHeader, StatCard } from "../components/shared";
import { Home } from "lucide-react";

export default function HospitalityPage() {
  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="Guest Relations Integrator"
        subtitle="Manage your hospitality operations"
      />
      <div className="card p-8 text-center text-gray-400">
        <Home size={40} className="mx-auto mb-3 text-pink-300" />
        <p className="text-sm font-medium text-gray-600">Guest Relations Integrator</p>
        <p className="text-xs mt-1">Full dashboard coming — API is live at /api/hospitality/</p>
      </div>
    </div>
  );
}
