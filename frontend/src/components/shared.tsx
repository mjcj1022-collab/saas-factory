import React from "react";
import { Link, useLocation } from "react-router-dom";
import {
  FileText, Building2, Store, Truck, Sun, Home,
  Calendar, Package, Briefcase, Leaf, Settings,
  Bell, LogOut, ChevronRight, BarChart3,
} from "lucide-react";
import { useAuthStore } from "../store/auth";

const NAV_ITEMS = [
  { label: "RFP Matrix", icon: FileText, path: "/rfp", color: "text-violet-500" },
  { label: "Construction", icon: Building2, path: "/construction", color: "text-orange-500" },
  { label: "Franchise", icon: Store, path: "/franchise", color: "text-green-500" },
  { label: "Fleet", icon: Truck, path: "/fleet", color: "text-blue-500" },
  { label: "Solar", icon: Sun, path: "/solar", color: "text-yellow-500" },
  { label: "Hospitality", icon: Home, path: "/hospitality", color: "text-pink-500" },
  { label: "Venue", icon: Calendar, path: "/venue", color: "text-cyan-500" },
  { label: "Sourcing", icon: Package, path: "/sourcing", color: "text-indigo-500" },
  { label: "Agency", icon: Briefcase, path: "/agency", color: "text-rose-500" },
  { label: "Food Supply", icon: Leaf, path: "/food", color: "text-emerald-500" },
];

export function Sidebar() {
  const location = useLocation();
  const { user, logout } = useAuthStore();

  return (
    <aside className="fixed inset-y-0 left-0 w-60 bg-gray-900 flex flex-col z-30">
      {/* Logo */}
      <div className="flex items-center gap-2 px-5 py-4 border-b border-gray-800">
        <div className="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center">
          <BarChart3 size={16} className="text-white" />
        </div>
        <span className="font-semibold text-white text-sm">SaaS Factory</span>
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
        {NAV_ITEMS.map((item) => {
          const active = location.pathname.startsWith(item.path);
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                active
                  ? "bg-gray-800 text-white"
                  : "text-gray-400 hover:bg-gray-800 hover:text-white"
              }`}
            >
              <item.icon size={16} className={active ? item.color : ""} />
              {item.label}
              {active && <ChevronRight size={14} className="ml-auto text-gray-600" />}
            </Link>
          );
        })}
      </nav>

      {/* User */}
      <div className="border-t border-gray-800 p-3">
        <div className="flex items-center gap-2 px-2 mb-2">
          <div className="w-7 h-7 rounded-full bg-brand-500 flex items-center justify-center text-white text-xs font-bold">
            {user?.first_name?.[0]}{user?.last_name?.[0]}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-white text-xs font-medium truncate">{user?.first_name} {user?.last_name}</p>
            <p className="text-gray-500 text-xs truncate">{user?.email}</p>
          </div>
        </div>
        <button
          onClick={logout}
          className="flex items-center gap-2 w-full px-3 py-1.5 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg text-xs transition-colors"
        >
          <LogOut size={13} />
          Sign out
        </button>
      </div>
    </aside>
  );
}

// ─── Stat Card ────────────────────────────────────────────────────────────────
interface StatCardProps {
  label: string;
  value: string | number;
  sub?: string;
  icon?: React.ReactNode;
  trend?: "up" | "down" | "neutral";
}

export function StatCard({ label, value, sub, icon, trend }: StatCardProps) {
  return (
    <div className="card p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs text-gray-500 font-medium uppercase tracking-wide">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
        </div>
        {icon && (
          <div className="w-9 h-9 rounded-lg bg-brand-50 flex items-center justify-center text-brand-500">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Status Badge ─────────────────────────────────────────────────────────────
const STATUS_STYLES: Record<string, string> = {
  // Generic
  active: "bg-green-100 text-green-700",
  inactive: "bg-gray-100 text-gray-600",
  pending: "bg-yellow-100 text-yellow-700",
  completed: "bg-blue-100 text-blue-700",
  failed: "bg-red-100 text-red-700",
  canceled: "bg-gray-100 text-gray-500",
  // RFP
  uploaded: "bg-gray-100 text-gray-600",
  parsing: "bg-yellow-100 text-yellow-700",
  generating: "bg-purple-100 text-purple-700",
  review: "bg-orange-100 text-orange-700",
  approved: "bg-green-100 text-green-700",
  exported: "bg-blue-100 text-blue-700",
  // Vehicles
  good: "bg-green-100 text-green-700",
  warning: "bg-yellow-100 text-yellow-700",
  critical: "bg-red-100 text-red-700",
  // Work orders
  open: "bg-orange-100 text-orange-700", // work orders
  in_progress: "bg-blue-100 text-blue-700",
  waiting_parts: "bg-purple-100 text-purple-700",
  // Franchise
  pipeline: "bg-gray-100 text-gray-600",
  site_selection: "bg-yellow-100 text-yellow-700",
  construction: "bg-orange-100 text-orange-700",
  training: "bg-purple-100 text-purple-700",
  pre_open: "bg-blue-100 text-blue-700",
  franchise_open: "bg-green-100 text-green-700",
};

export function StatusBadge({ status }: { status: string }) {
  const cls = STATUS_STYLES[status] ?? "bg-gray-100 text-gray-600";
  return (
    <span className={`badge ${cls}`}>
      {status.replace(/_/g, " ")}
    </span>
  );
}

// ─── Page Header ─────────────────────────────────────────────────────────────
export function PageHeader({
  title, subtitle, action,
}: {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex items-start justify-between mb-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">{title}</h1>
        {subtitle && <p className="text-sm text-gray-500 mt-0.5">{subtitle}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}

// ─── Empty State ─────────────────────────────────────────────────────────────
export function EmptyState({ icon, title, description, action }: {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      {icon && <div className="text-gray-300 mb-3">{icon}</div>}
      <h3 className="text-sm font-semibold text-gray-900">{title}</h3>
      {description && <p className="text-sm text-gray-400 mt-1 max-w-sm">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

// ─── Loading Spinner ──────────────────────────────────────────────────────────
export function Spinner({ size = 20 }: { size?: number }) {
  return (
    <div
      className="animate-spin rounded-full border-2 border-gray-200 border-t-brand-500"
      style={{ width: size, height: size }}
    />
  );
}
