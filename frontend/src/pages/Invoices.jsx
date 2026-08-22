import { useEffect, useState } from "react";

import DataTable from "../components/DataTable";
import { getInvoices } from "../services/api";

function Invoices() {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    getInvoices()
      .then((response) => setInvoices(response.data))
      .catch(console.error);
  }, []);

  const columns = [
    { key: "invoice_id", label: "Invoice ID" },
    { key: "email_id", label: "Email ID" },
    { key: "vendor", label: "Vendor" },
    { key: "amount", label: "Amount" },
    { key: "currency", label: "Currency" },
    { key: "status", label: "Status" },
    { key: "created_at", label: "Created At" },
  ];

  return (
    <div className="page">
      <h1>Invoices</h1>
      <p>Invoices processed by the AI agent.</p>

      <DataTable columns={columns} data={invoices} />
    </div>
  );
}

export default Invoices;