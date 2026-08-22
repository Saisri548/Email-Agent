import { useState } from "react";
import { processEmail } from "../services/api";

function EmailForm({ onProcessed }) {
  const [sender, setSender] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const email = {
        id: crypto.randomUUID(),
        sender,
        subject,
        body,
      };

      const result = await processEmail(email);

      onProcessed(result);

      setSender("");
      setSubject("");
      setBody("");
    } catch (error) {
      console.error(error);
      setError(
        error.response?.data?.detail ||
          "Failed to process email."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-card">
      <div className="section-header">
        <div>
          <h2>Process New Email</h2>
          <p>
            Submit an email and let the AI agent analyze and
            execute the appropriate action.
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <label>Sender</label>

        <input
          type="email"
          placeholder="billing@example.com"
          value={sender}
          onChange={(e) => setSender(e.target.value)}
          required
        />

        <label>Subject</label>

        <input
          type="text"
          placeholder="Invoice INV-1001"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          required
        />

        <label>Email Body</label>

        <textarea
          rows="7"
          placeholder="Please process invoice INV-1001 for USD 2500..."
          value={body}
          onChange={(e) => setBody(e.target.value)}
          required
        />

        {error && <div className="error">{error}</div>}

        <button
          className="primary-button"
          type="submit"
          disabled={loading}
        >
          {loading ? "🤖 Processing..." : "Process Email"}
        </button>
      </form>
    </div>
  );
}

export default EmailForm;