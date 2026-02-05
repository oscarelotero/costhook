import { supabase } from "./supabase";

const API_BASE = "/api/v1";

async function getAuthHeaders(): Promise<HeadersInit> {
  const {
    data: { session },
  } = await supabase.auth.getSession();
  if (!session) {
    throw new Error("Not authenticated");
  }
  return {
    Authorization: `Bearer ${session.access_token}`,
    "Content-Type": "application/json",
  };
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: { ...headers, ...options.headers },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export const api = {
  // Users
  getProfile: () => request<UserProfile>("/users/me"),
  updateProfile: (data: UserProfileUpdate) =>
    request<UserProfile>("/users/me", {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  // Providers
  listProviders: () => request<Provider[]>("/providers"),
  createProvider: (data: ProviderCreate) =>
    request<Provider>("/providers", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  getProvider: (id: string) => request<Provider>(`/providers/${id}`),
  updateProvider: (id: string, data: ProviderUpdate) =>
    request<Provider>(`/providers/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  deleteProvider: (id: string) =>
    request<void>(`/providers/${id}`, { method: "DELETE" }),

  // Costs
  listCosts: (params?: CostFilters) => {
    const searchParams = new URLSearchParams();
    if (params?.provider_id) searchParams.set("provider_id", params.provider_id);
    if (params?.provider_type)
      searchParams.set("provider_type", params.provider_type);
    if (params?.start_date) searchParams.set("start_date", params.start_date);
    if (params?.end_date) searchParams.set("end_date", params.end_date);
    const query = searchParams.toString();
    return request<CostRecord[]>(`/costs${query ? `?${query}` : ""}`);
  },
};

// Types
export interface UserProfile {
  id: string;
  auth_user_id: string;
  display_name: string | null;
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface UserProfileUpdate {
  display_name?: string | null;
  timezone?: string | null;
}

export type ProviderType =
  | "supabase"
  | "vercel"
  | "resend"
  | "stripe"
  | "openai"
  | "anthropic";

export type ProviderStatus = "connected" | "error" | "syncing" | "pending";

export interface Provider {
  id: string;
  user_id: string;
  type: ProviderType;
  name: string;
  status: ProviderStatus;
  last_sync_at: string | null;
  last_error: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProviderCreate {
  name: string;
  type: ProviderType;
  credentials: Record<string, string>;
}

export interface ProviderUpdate {
  name?: string;
  credentials?: Record<string, string>;
}

export interface CostRecord {
  id: string;
  provider_id: string;
  amount: number;
  service: string;
  period_start: string;
  period_end: string;
  metadata_json: string | null;
  created_at: string;
}

export interface CostFilters {
  provider_id?: string;
  provider_type?: ProviderType;
  start_date?: string;
  end_date?: string;
}
