import { PageHeader, StatCard } from "../components/shared";
import { Briefcase } from "lucide-react";

export default function AgencyPage() {
  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="Agency Deliverable Matrix"
        subtitle="Manage your agency operations"
      />
      <div className="card p-8 text-center text-gray-400">
        <Briefcase size={40} className="mx-auto mb-3 text-rose-300" />
        <p className="text-sm font-medium text-gray-600">Agency Deliverable Matrix</p>
        <p className="text-xs mt-1">Full dashboard coming — API is live at /api/agency/</p>
      </div>
    </div>
  );
}
