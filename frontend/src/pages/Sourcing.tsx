import { PageHeader, StatCard } from "../components/shared";
import { Package } from "lucide-react";

export default function SourcingPage() {
  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="Manufacturer Sourcing Pipeline"
        subtitle="Manage your sourcing operations"
      />
      <div className="card p-8 text-center text-gray-400">
        <Package size={40} className="mx-auto mb-3 text-indigo-300" />
        <p className="text-sm font-medium text-gray-600">Manufacturer Sourcing Pipeline</p>
        <p className="text-xs mt-1">Full dashboard coming — API is live at /api/sourcing/</p>
      </div>
    </div>
  );
}
