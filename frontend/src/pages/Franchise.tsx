import { PageHeader, StatCard } from "../components/shared";
import { Store } from "lucide-react";

export default function FranchisePage() {
  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="Franchise Onboarding Hub"
        subtitle="Manage your franchise operations"
      />
      <div className="card p-8 text-center text-gray-400">
        <Store size={40} className="mx-auto mb-3 text-green-300" />
        <p className="text-sm font-medium text-gray-600">Franchise Onboarding Hub</p>
        <p className="text-xs mt-1">Full dashboard coming — API is live at /api/franchise/</p>
      </div>
    </div>
  );
}
