import { PageHeader, StatCard } from "../components/shared";
import { Sun } from "lucide-react";

export default function SolarPage() {
  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="Solar Compliance Engine"
        subtitle="Manage your solar operations"
      />
      <div className="card p-8 text-center text-gray-400">
        <Sun size={40} className="mx-auto mb-3 text-yellow-300" />
        <p className="text-sm font-medium text-gray-600">Solar Compliance Engine</p>
        <p className="text-xs mt-1">Full dashboard coming — API is live at /api/solar/</p>
      </div>
    </div>
  );
}
