import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Inject auth token on every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Global 401 handler — redirect to login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("auth_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// ─── Auth ────────────────────────────────────────────────────────────────────
export const authAPI = {
  login: (email: string, password: string) =>
    api.post("/auth/login/", { email, password }),
  register: (data: object) => api.post("/auth/register/", data),
  me: () => api.get("/auth/users/me/"),
};

// ─── RFP ─────────────────────────────────────────────────────────────────────
export const rfpAPI = {
  list: (params?: object) => api.get("/rfp/requests/", { params }),
  get: (id: string) => api.get(`/rfp/requests/${id}/`),
  create: (data: FormData) =>
    api.post("/rfp/requests/", data, { headers: { "Content-Type": "multipart/form-data" } }),
  generate: (id: string) => api.post(`/rfp/requests/${id}/generate/`),
  export: (id: string, format = "docx") => api.post(`/rfp/requests/${id}/export/`, { format }),
  stats: (id: string) => api.get(`/rfp/requests/${id}/stats/`),
  knowledge: {
    list: () => api.get("/rfp/knowledge/"),
    upload: (data: FormData) =>
      api.post("/rfp/knowledge/", data, { headers: { "Content-Type": "multipart/form-data" } }),
  },
  responses: {
    approve: (id: string, notes?: string) => api.post(`/rfp/responses/${id}/approve/`, { notes }),
    requestRevision: (id: string, notes: string) =>
      api.post(`/rfp/responses/${id}/request_revision/`, { notes }),
  },
};

// ─── Fleet ───────────────────────────────────────────────────────────────────
export const fleetAPI = {
  vehicles: {
    list: () => api.get("/fleet/vehicles/"),
    create: (data: object) => api.post("/fleet/vehicles/", data),
    analyze: (id: string) => api.post(`/fleet/vehicles/${id}/analyze/`),
    health: () => api.get("/fleet/vehicles/fleet_health/"),
  },
  workOrders: {
    list: () => api.get("/fleet/work-orders/"),
    create: (data: object) => api.post("/fleet/work-orders/", data),
    complete: (id: string, data: object) => api.post(`/fleet/work-orders/${id}/complete/`, data),
  },
  inventory: {
    list: () => api.get("/fleet/inventory/"),
    lowStock: () => api.get("/fleet/inventory/low_stock/"),
  },
};

// ─── Construction ─────────────────────────────────────────────────────────────
export const constructionAPI = {
  projects: {
    list: () => api.get("/construction/projects/"),
    create: (data: object) => api.post("/construction/projects/", data),
    get: (id: string) => api.get(`/construction/projects/${id}/`),
  },
  drawings: {
    list: (projectId?: string) =>
      api.get("/construction/drawings/", { params: projectId ? { project: projectId } : {} }),
    upload: (data: FormData) =>
      api.post("/construction/drawings/", data, { headers: { "Content-Type": "multipart/form-data" } }),
  },
  revisions: { list: () => api.get("/construction/revisions/") },
  punchItems: { list: () => api.get("/construction/punch-items/") },
};

// ─── Franchise ───────────────────────────────────────────────────────────────
export const franchiseAPI = {
  brands: {
    list: () => api.get("/franchise/brands/"),
    create: (data: object) => api.post("/franchise/brands/", data),
  },
  franchisees: {
    list: () => api.get("/franchise/franchisees/"),
    create: (data: object) => api.post("/franchise/franchisees/", data),
  },
  locations: {
    list: () => api.get("/franchise/locations/"),
    pipeline: () => api.get("/franchise/locations/pipeline/"),
    advance: (id: string) => api.post(`/franchise/locations/${id}/advance_stage/`),
  },
  milestones: {
    list: () => api.get("/franchise/milestones/"),
    complete: (id: string) => api.post(`/franchise/milestones/${id}/complete/`),
  },
};

// ─── Hospitality ─────────────────────────────────────────────────────────────
export const hospitalityAPI = {
  properties: {
    list: () => api.get("/hospitality/rentalpropertys/"),
    create: (data: object) => api.post("/hospitality/rentalpropertys/", data),
  },
  reservations: {
    list: () => api.get("/hospitality/reservations/"),
    create: (data: object) => api.post("/hospitality/reservations/", data),
  },
  cleaningJobs: { list: () => api.get("/hospitality/cleaningjobs/") },
};

// ─── Solar ───────────────────────────────────────────────────────────────────
export const solarAPI = {
  properties: {
    list: () => api.get("/solar/propertys/"),
    create: (data: object) => api.post("/solar/propertys/", data),
  },
  permits: {
    list: () => api.get("/solar/permits/"),
    create: (data: object) => api.post("/solar/permits/", data),
  },
  inspections: { list: () => api.get("/solar/inspections/") },
};

// ─── Venue ───────────────────────────────────────────────────────────────────
export const venueAPI = {
  venues: { list: () => api.get("/venue/venues/") },
  bookings: {
    list: () => api.get("/venue/venuebookings/"),
    create: (data: object) => api.post("/venue/venuebookings/", data),
  },
  invoices: { list: () => api.get("/venue/venueinvoices/") },
};

// ─── Sourcing ─────────────────────────────────────────────────────────────────
export const sourcingAPI = {
  suppliers: { list: () => api.get("/sourcing/suppliers/") },
  products: { list: () => api.get("/sourcing/products/") },
  quotes: { list: () => api.get("/sourcing/supplierquotes/") },
  runs: { list: () => api.get("/sourcing/productionruns/") },
};

// ─── Agency ───────────────────────────────────────────────────────────────────
export const agencyAPI = {
  clients: { list: () => api.get("/agency/clients/") },
  projects: { list: () => api.get("/agency/agencyprojects/") },
  assets: {
    list: () => api.get("/agency/assets/"),
    create: (data: object) => api.post("/agency/assets/", data),
  },
  invoices: { list: () => api.get("/agency/agencyinvoices/") },
};

// ─── Food ─────────────────────────────────────────────────────────────────────
export const foodAPI = {
  farms: { list: () => api.get("/food/farms/") },
  harvests: { list: () => api.get("/food/harvstlogs/") },
  routes: { list: () => api.get("/food/deliveryroutes/") },
  stores: { list: () => api.get("/food/stores/") },
};
