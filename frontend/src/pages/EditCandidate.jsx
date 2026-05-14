import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../api/client";
import Button from "../components/Button";

export default function EditCandidate() {
  const { id } = useParams();
  const nav = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    role_applied: "",
    skills: ""
  });

  const [loading, setLoading] = useState(false);

  // fetch candidate
  useEffect(() => {
    const load = async () => {
      const res = await API.get(`/candidates/${id}`);
      setForm({
        name: res.data.name,
        email: res.data.email,
        role_applied: res.data.role_applied,
        skills: res.data.skills.join(",")
      });
    };

    load();
  }, [id]);

  const update = async () => {
    try {
      setLoading(true);

      await API.put(`/candidates/${id}`, {
        ...form,
        skills: form.skills.split(",")
      });

      nav("/candidates");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2>Edit Candidate</h2>

        <input
          style={styles.input}
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          placeholder="Name"
        />

        <input
          style={styles.input}
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          placeholder="Email"
        />

        <input
          style={styles.input}
          value={form.role_applied}
          onChange={(e) =>
            setForm({ ...form, role_applied: e.target.value })
          }
          placeholder="Role"
        />

        <input
          style={styles.input}
          value={form.skills}
          onChange={(e) => setForm({ ...form, skills: e.target.value })}
          placeholder="Skills (comma separated)"
        />

        <div style={{ marginTop: 12 }}>
          <Button onClick={update} disabled={loading}>
            {loading ? "Updating..." : "Update"}
          </Button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#0f172a"
  },
  card: {
    width: 400,
    padding: 20,
    borderRadius: 12,
    background: "white"
  },
  input: {
    width: "100%",
    padding: 10,
    marginTop: 10,
    border: "1px solid #ccc",
    borderRadius: 8
  }
};