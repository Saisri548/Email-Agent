import { useEffect, useState } from "react";

import StatCard from "../components/StatCard";
import EmailForm from "../components/EmailForm";
import { getDashboard } from "../services/api";

function Dashboard() {
  const [stats, setStats] = useState({
    emails: 0,
    invoices: 0,
    tasks: 0,
    disputes: 0,
    audit_logs: 0,
  });

  const [result, setResult] = useState(null);

  const loadDashboard = async () => {
    try {
      const response = await getDashboard();
      setStats(response.statistics);
    } catch (error) {
      console.error("Dashboard error:", error);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const handleProcessed = async (data) => {
    setResult(data);
    await loadDashboard();
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>
            Monitor your autonomous email processing system.
          </p>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Emails"
          value={stats.emails}
          icon="📧"
        />

        <StatCard
          title="Invoices"
          value={stats.invoices}
          icon="🧾"
        />

        <StatCard
          title="Tasks"
          value={stats.tasks}
          icon="📋"
        />

        <StatCard
          title="Disputes"
          value={stats.disputes}
          icon="⚠️"
        />

        <StatCard
          title="Audit Logs"
          value={stats.audit_logs}
          icon="🔍"
        />
      </div>

      <EmailForm onProcessed={handleProcessed} />

      {result && (
        <div className="result-card">
          <h2>AI Processing Result</h2>

          <div className="result-grid">
            <div>
              <span>Intent</span>
              <strong>{result.classification.intent}</strong>
            </div>

            <div>
              <span>Confidence</span>
              <strong>
                {(result.classification.confidence * 100).toFixed(0)}%
              </strong>
            </div>

            <div>
              <span>Action</span>
              <strong>{result.action.name}</strong>
            </div>

            <div>
              <span>Human Review</span>
              <strong>
                {result.action.requires_human_review
                  ? "Required"
                  : "Not Required"}
              </strong>
            </div>
          </div>

          <div className="result-section">
            <span>Result</span>
            <p>{result.action.result}</p>
          </div>

          <div className="result-section">
            <span>Reasoning</span>
            <p>{result.classification.reasoning}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;