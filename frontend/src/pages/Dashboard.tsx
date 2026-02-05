import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api, Provider, CostRecord } from "../lib/api";

export default function Dashboard() {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [costs, setCosts] = useState<CostRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [providersData, costsData] = await Promise.all([
        api.listProviders(),
        api.listCosts(),
      ]);
      setProviders(providersData);
      setCosts(costsData);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  const totalCost = costs.reduce((sum, cost) => sum + cost.amount, 0);

  if (loading) {
    return <div className="page-container">Loading...</div>;
  }

  return (
    <div className="page-container">
      <h1>Dashboard</h1>

      <div className="dashboard-grid">
        <div className="card stat-card">
          <h3>Total Spend</h3>
          <p className="stat-value">${totalCost.toFixed(2)}</p>
        </div>

        <div className="card stat-card">
          <h3>Providers</h3>
          <p className="stat-value">{providers.length}</p>
        </div>

        <div className="card stat-card">
          <h3>Cost Records</h3>
          <p className="stat-value">{costs.length}</p>
        </div>
      </div>

      {providers.length === 0 ? (
        <div className="card empty-state">
          <h2>Get Started</h2>
          <p>Connect your first provider to start tracking costs.</p>
          <Link to="/providers" className="btn-primary">
            Add Provider
          </Link>
        </div>
      ) : (
        <div className="card">
          <h2>Recent Costs</h2>
          {costs.length === 0 ? (
            <p>No cost data yet. Sync your providers to see costs.</p>
          ) : (
            <table className="costs-table">
              <thead>
                <tr>
                  <th>Service</th>
                  <th>Amount</th>
                  <th>Period</th>
                </tr>
              </thead>
              <tbody>
                {costs.slice(0, 10).map((cost) => (
                  <tr key={cost.id}>
                    <td>{cost.service}</td>
                    <td>${cost.amount.toFixed(2)}</td>
                    <td>
                      {new Date(cost.period_start).toLocaleDateString()} -{" "}
                      {new Date(cost.period_end).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
