import { useEffect, useState } from "react";

import DataTable from "../components/DataTable";
import { getEmails } from "../services/api";

function Emails() {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    getEmails()
      .then((response) => setEmails(response.data))
      .catch(console.error);
  }, []);

  const columns = [
    { key: "email_id", label: "Email ID" },
    { key: "sender", label: "Sender" },
    { key: "subject", label: "Subject" },
    { key: "received_at", label: "Received At" },
  ];

  return (
    <div className="page">
      <h1>Emails</h1>
      <p>All processed emails.</p>

      <DataTable columns={columns} data={emails} />
    </div>
  );
}

export default Emails;