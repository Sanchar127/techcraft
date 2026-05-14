import React, { useEffect, useState } from "react";
import API from "../api/client";
import { useNavigate } from "react-router-dom";

export default function Candidates() {
  const [data, setData] = useState([]);
  const nav = useNavigate();

  const fetchCandidates = async () => {
    const res = await API.get("/candidates?skip=0&limit=20");
    setData(res.data.data);
  };

  const deleteCandidate = async (id) => {
    await API.delete(`/candidates/${id}`);
    fetchCandidates();
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  return (
    <div style={styles.page}>
      <h2 style={styles.title}>Candidates</h2>

      <div style={styles.grid}>
        {data.map((c) => (
          <div key={c.id} style={styles.card}>
            
            {/* Candidate Info */}
            <div>
              <h3 style={styles.name}>{c.name}</h3>
              <p style={styles.text}>{c.email}</p>
              <p style={styles.text}>{c.role_applied}</p>
            </div>

            {/* VIEW DETAILS LINK (IMPORTANT UX) */}
            <div
              style={styles.link}
              onClick={() => nav(`/candidates/${c.id}`)}
            >
              View Details →
            </div>

            {/* ACTIONS */}
            <div style={styles.actions}>
              <button
                style={styles.editBtn}
                onClick={(e) => {
                  e.stopPropagation();
                  nav(`/edit/${c.id}`);
                }}
              >
                Edit
              </button>

              <button
                style={styles.deleteBtn}
                onClick={(e) => {
                  e.stopPropagation();
                  deleteCandidate(c.id);
                }}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  page: {
    padding: "30px",
    fontFamily: "system-ui",
    background: "#0f172a",
    minHeight: "100vh",
    color: "white"
  },

  title: {
    fontSize: "24px",
    marginBottom: "20px"
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    gap: "15px"
  },

  card: {
    background: "#1e293b",
    padding: "15px",
    borderRadius: "10px"
  },

  name: {
    margin: "0 0 6px 0"
  },

  text: {
    margin: "2px 0",
    opacity: 0.8,
    fontSize: "14px"
  },

  link: {
    marginTop: "10px",
    color: "#60a5fa",
    cursor: "pointer",
    fontSize: "14px",
    fontWeight: "500"
  },

  actions: {
    marginTop: "12px",
    display: "flex",
    gap: "10px"
  },

  editBtn: {
    flex: 1,
    padding: "6px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    background: "#3b82f6",
    color: "white"
  },

  deleteBtn: {
    flex: 1,
    padding: "6px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    background: "#ef4444",
    color: "white"
  }
};