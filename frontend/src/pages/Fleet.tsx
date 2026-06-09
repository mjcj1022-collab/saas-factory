import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Truck, AlertTriangle, CheckCircle, Wrench, Package, Zap } from "lucide-react";
import { fleetAPI } from "../lib/api";
import { PageHeader, StatCard, StatusBadge, EmptyState, Spinner } from "../components/shared";

export default function FleetPage() {
  const qc = useQueryClient();

  const { data: vehicles, isLoading } = useQuery({
    queryKey: ["vehicles"],
    queryFn: () => fleetAPI.vehicles.list().then((r) => r.data.results ?? r.data),
  });
  const { data: health } = useQuery({
    queryKey: ["fleet-health"],
    queryFn: () => fleetAPI.vehicles.health().then((r) => r.data),
  });
  const { data: workOrders } = useQuery({
    queryKey: ["work-orders"],
    queryFn: () => fleetAPI.workOrders.list().then((r) => r.data.results ?? r.data),
  });
  const { data: lowStock } = useQuery({
    queryKey: ["low-stock"],
    queryFn: () => fleetAPI.inventory.lowStock().then((r) => r.data.results ?? r.data),
  });

  const analyzeMutation = useMutation({
    mutationFn: (id: string) => fleetAPI.vehicles.analyze(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["vehicles"] });
      qc.invalidateQueries({ queryKey: ["fleet-health"] });
    },
  });

  const completeMutation = useMutation({
    mutationFn: (id: string) => fleetAPI.workOrders.complete(id, {}),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["work-orders"] }),
  });

  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="Fleet Maintenance Optimizer"
        subtitle="Predictive maintenance, work orders, and inventory management"
      />

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <StatCard label="Total Vehicles" value={health?.total ?? 0} icon={<Truck size={18} />} />
        <StatCard label="Critical" value={health?.critical ?? 0} icon={<AlertTriangle size={18} />} sub="Require attention" />
        <StatCard label="Healthy" value={health?.healthy ?? 0} icon={<CheckCircle size={18} />} />
        <StatCard label="Low Stock Parts" value={lowStock?.length ?? 0} icon={<Package size={18} />} />
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Vehicles */}
        <div className="card overflow-hidden">
          <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-gray-900">Vehicle Fleet</h2>
            <span className="text-xs text-gray-400">{vehicles?.length ?? 0} vehicles</span>
          </div>
          {isLoading ? (
            <div className="flex justify-center py-10"><Spinner /></div>
          ) : !vehicles?.length ? (
            <EmptyState icon={<Truck size={32} />} title="No vehicles registered" />
          ) : (
            <div className="divide-y divide-gray-50 max-h-80 overflow-y-auto">
              {vehicles.map((v: any) => (
                <div key={v.id} className="px-4 py-3 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{v.year} {v.make} {v.model}</p>
                    <p className="text-xs text-gray-400">{v.vin.slice(-8)} · {v.odometer?.toLocaleString()} mi · {v.open_work_orders} open WO</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <StatusBadge status={v.health_score} />
                    <button
                      onClick={() => analyzeMutation.mutate(v.id)}
                      disabled={analyzeMutation.isPending}
                      className="btn-secondary py-1 px-2 text-xs"
                    >
                      <Zap size={11} />
                      Analyze
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Open Work Orders */}
        <div className="card overflow-hidden">
          <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-gray-900">Open Work Orders</h2>
          </div>
          {!workOrders?.length ? (
            <EmptyState icon={<Wrench size={32} />} title="No open work orders" />
          ) : (
            <div className="divide-y divide-gray-50 max-h-80 overflow-y-auto">
              {workOrders
                .filter((wo: any) => wo.status !== "completed" && wo.status !== "canceled")
                .map((wo: any) => (
                <div key={wo.id} className="px-4 py-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">{wo.description}</p>
                      <p className="text-xs text-gray-400 mt-0.5">{wo.vehicle_info}</p>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <StatusBadge status={wo.status} />
                      {wo.status !== "completed" && (
                        <button
                          onClick={() => completeMutation.mutate(wo.id)}
                          className="btn-secondary py-1 px-2 text-xs"
                        >
                          Complete
                        </button>
                      )}
                    </div>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">
                    Est. ${parseFloat(wo.estimated_cost).toLocaleString()}
                    {wo.scheduled_date && ` · Scheduled ${wo.scheduled_date}`}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Low Stock Alert */}
        {lowStock?.length > 0 && (
          <div className="card overflow-hidden col-span-2">
            <div className="px-4 py-3 border-b border-gray-100 flex items-center gap-2">
              <AlertTriangle size={14} className="text-amber-500" />
              <h2 className="text-sm font-semibold text-gray-900">Low Stock Parts — Reorder Needed</h2>
            </div>
            <div className="divide-y divide-gray-50">
              {lowStock.map((part: any) => (
                <div key={part.id} className="px-4 py-3 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{part.name}</p>
                    <p className="text-xs text-gray-400">SKU: {part.sku} · Supplier: {part.supplier || "N/A"}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-bold text-red-600">{part.quantity} remaining</p>
                    <p className="text-xs text-gray-400">Reorder at {part.reorder_point}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
