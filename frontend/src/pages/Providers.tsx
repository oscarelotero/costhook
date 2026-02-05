import { useState, useEffect } from "react";
import { api, Provider, ProviderType } from "../lib/api";

const PROVIDER_LABELS: Record<ProviderType, string> = {
  supabase: "Supabase",
  vercel: "Vercel",
  resend: "Resend",
  stripe: "Stripe",
  openai: "OpenAI",
  anthropic: "Anthropic",
};

const PROVIDER_CREDENTIALS: Record<ProviderType, { key: string; label: string; placeholder: string }[]> = {
  supabase: [
    { key: "access_token", label: "Access Token", placeholder: "sbp_..." },
    { key: "org_id", label: "Organization ID", placeholder: "org-..." },
  ],
  vercel: [
    { key: "api_token", label: "API Token", placeholder: "..." },
    { key: "team_id", label: "Team ID (optional)", placeholder: "team_..." },
  ],
  resend: [
    { key: "api_key", label: "API Key", placeholder: "re_..." },
  ],
  stripe: [
    { key: "api_key", label: "Secret Key", placeholder: "sk_..." },
  ],
  openai: [
    { key: "api_key", label: "API Key", placeholder: "sk-..." },
    { key: "org_id", label: "Organization ID (optional)", placeholder: "org-..." },
  ],
  anthropic: [
    { key: "api_key", label: "API Key", placeholder: "sk-ant-..." },
  ],
};

export default function Providers() {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: "",
    type: "supabase" as ProviderType,
    credentials: {} as Record<string, string>,
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadProviders();
  }, []);

  const loadProviders = async () => {
    try {
      const data = await api.listProviders();
      setProviders(data);
    } catch (err) {
      console.error("Failed to load providers:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError("");

    try {
      if (editingId) {
        await api.updateProvider(editingId, {
          name: formData.name,
          credentials: formData.credentials,
        });
      } else {
        await api.createProvider(formData);
      }
      await loadProviders();
      resetForm();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save provider");
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (provider: Provider) => {
    setEditingId(provider.id);
    setFormData({
      name: provider.name,
      type: provider.type,
      credentials: {},
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this provider?")) return;

    try {
      await api.deleteProvider(id);
      await loadProviders();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to delete");
    }
  };

  const resetForm = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData({ name: "", type: "supabase", credentials: {} });
    setError("");
  };

  const getStatusBadge = (status: string) => {
    const colors: Record<string, string> = {
      connected: "badge-success",
      error: "badge-error",
      syncing: "badge-warning",
      pending: "badge-pending",
    };
    return <span className={`badge ${colors[status] || ""}`}>{status}</span>;
  };

  if (loading) {
    return <div className="page-container">Loading...</div>;
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Providers</h1>
        {!showForm && (
          <button onClick={() => setShowForm(true)}>Add Provider</button>
        )}
      </div>

      {showForm && (
        <div className="card">
          <h2>{editingId ? "Edit Provider" : "Add Provider"}</h2>
          {error && <div className="error">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input
                id="name"
                type="text"
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                placeholder="My Vercel Account"
                required
              />
            </div>

            {!editingId && (
              <div className="form-group">
                <label htmlFor="type">Provider Type</label>
                <select
                  id="type"
                  value={formData.type}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      type: e.target.value as ProviderType,
                      credentials: {},
                    })
                  }
                >
                  {Object.entries(PROVIDER_LABELS).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {PROVIDER_CREDENTIALS[formData.type].map((field) => (
              <div className="form-group" key={field.key}>
                <label htmlFor={field.key}>{field.label}</label>
                <input
                  id={field.key}
                  type="password"
                  value={formData.credentials[field.key] || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      credentials: {
                        ...formData.credentials,
                        [field.key]: e.target.value,
                      },
                    })
                  }
                  placeholder={field.placeholder}
                />
              </div>
            ))}

            <div className="form-actions">
              <button type="button" onClick={resetForm} className="btn-secondary">
                Cancel
              </button>
              <button type="submit" disabled={saving}>
                {saving ? "Saving..." : editingId ? "Update" : "Add Provider"}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="providers-list">
        {providers.length === 0 ? (
          <div className="empty-state">
            <p>No providers connected yet.</p>
            <p>Add a provider to start tracking costs.</p>
          </div>
        ) : (
          providers.map((provider) => (
            <div key={provider.id} className="card provider-card">
              <div className="provider-header">
                <div>
                  <h3>{provider.name}</h3>
                  <span className="provider-type">
                    {PROVIDER_LABELS[provider.type]}
                  </span>
                </div>
                {getStatusBadge(provider.status)}
              </div>
              {provider.last_sync_at && (
                <p className="last-sync">
                  Last synced: {new Date(provider.last_sync_at).toLocaleString()}
                </p>
              )}
              {provider.last_error && (
                <p className="provider-error">{provider.last_error}</p>
              )}
              <div className="provider-actions">
                <button onClick={() => handleEdit(provider)} className="btn-secondary">
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(provider.id)}
                  className="btn-danger"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
