import { PageHeader, StatCard } from "../components/shared";
import { Calendar } from "lucide-react";

export default function VenuePage() {
  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="Venue Operations Hub"
        subtitle="Manage your venue operations"
      />
      <div className="card p-8 text-center text-gray-400">
        <Calendar size={40} className="mx-auto mb-3 text-cyan-300" />
        <p className="text-sm font-medium text-gray-600">Venue Operations Hub</p>
        <p className="text-xs mt-1">Full dashboard coming — API is live at /api/venue/</p>
      </div>
    </div>
  );
}
