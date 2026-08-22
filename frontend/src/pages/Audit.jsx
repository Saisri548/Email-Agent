import { useEffect, useState } from "react";

import DataTable from "../components/DataTable";
import { getAuditLogs } from "../services/api";

function Audit() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    getAuditLogs()
      .then((response) => setLogs(response.data))
      .catch(console.error);
  }, []);

  const columns = [
    { key: "id", label: "ID" },
    { key: "email_id", label: "Email ID" },
    { key: "intent", label: "Intent" },
    { key: "confidence", label: "Confidence" },
    { key: "action", label: "Action" },
    { key: "reason", label: "Reason" },
    { key: "result", label: "Result" },
    { key: "timestamp", label: "Timestamp" },
  ];

  return (
    <div className="page">
      <h1>Audit Trail</h1>
      <p>Complete history of AI decisions and actions.</p>

      <DataTable columns={columns} data={logs} />
    </div>
  );
}

export default Audit;