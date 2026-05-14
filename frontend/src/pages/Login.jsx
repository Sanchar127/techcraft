import { useState } from "react";
import API from "../api/client";
import Button from "../components/Button";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const login = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await API.post("/auth/login", {
        email,
        password,
      });

      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/candidates";
    } catch (err) {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.wrapper}>
      <div style={styles.page}>
        <div style={styles.card}>
          <div style={styles.header}>
            <h1 style={styles.title}>TechKraft</h1>
            <p style={styles.subtitle}>Internal Admin Dashboard</p>
          </div>

          {error && <div style={styles.error}>{error}</div>}

          <div style={styles.form}>
            <label style={styles.label}>Email</label>
            <input
              style={styles.input}
              placeholder="admin@techkraft.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <label style={styles.label}>Password</label>
            <input
              style={styles.input}
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <div style={{ marginTop: "16px" }}>
              <Button onClick={login} disabled={loading}>
                {loading ? "Signing in..." : "Login"}
              </Button>
            </div>
          </div>

          <p style={styles.footer}>Secure internal system</p>
        </div>
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    position: "fixed",
    inset: 0,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #0f172a, #1e293b)",
  },

  page: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },

  card: {
    width: "380px",
    background: "#ffffff",
    borderRadius: "14px",
    padding: "28px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.35)",
  },

  header: {
    marginBottom: "18px",
    textAlign: "center",
  },

  title: {
    margin: 0,
    fontSize: "24px",
    fontWeight: "700",
    color: "#111827",
  },

  subtitle: {
    marginTop: "6px",
    fontSize: "13px",
    color: "#6b7280",
  },

  form: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },

  label: {
    fontSize: "12px",
    color: "#374151",
    marginTop: "10px",
  },

  input: {
    padding: "10px 12px",
    borderRadius: "8px",
    border: "1px solid #e5e7eb",
    outline: "none",
    fontSize: "14px",
  },

  error: {
    background: "#fee2e2",
    color: "#b91c1c",
    padding: "8px",
    borderRadius: "8px",
    fontSize: "13px",
    marginBottom: "10px",
  },

  footer: {
    marginTop: "18px",
    fontSize: "11px",
    textAlign: "center",
    color: "#9ca3af",
  },
};