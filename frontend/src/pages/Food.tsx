import { PageHeader, StatCard } from "../components/shared";
import { Leaf } from "lucide-react";

export default function FoodPage() {
  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="Food Supply Connector"
        subtitle="Manage your food operations"
      />
      <div className="card p-8 text-center text-gray-400">
        <Leaf size={40} className="mx-auto mb-3 text-emerald-300" />
        <p className="text-sm font-medium text-gray-600">Food Supply Connector</p>
        <p className="text-xs mt-1">Full dashboard coming — API is live at /api/food/</p>
      </div>
    </div>
  );
}
