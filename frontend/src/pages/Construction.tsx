import { PageHeader, StatCard } from "../components/shared";
import { Building2 } from "lucide-react";

export default function ConstructionPage() {
  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="Construction Liaison Platform"
        subtitle="Manage your construction operations"
      />
      <div className="card p-8 text-center text-gray-400">
        <Building2 size={40} className="mx-auto mb-3 text-orange-300" />
        <p className="text-sm font-medium text-gray-600">Construction Liaison Platform</p>
        <p className="text-xs mt-1">Full dashboard coming — API is live at /api/construction/</p>
      </div>
    </div>
  );
}
