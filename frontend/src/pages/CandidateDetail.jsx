import { useEffect, useState } from "react";
import API from "../api/client";
import { useParams, useNavigate } from "react-router-dom";
import Button from "../components/Button";

export default function CandidateDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [candidate, setCandidate] = useState(null);

  const [category, setCategory] = useState("");
  const [score, setScore] = useState(3);
  const [note, setNote] = useState("");

  const [message, setMessage] = useState("");

  const fetchCandidate = async () => {
    const res = await API.get(`/candidates/${id}`);
    setCandidate(res.data);
  };

  useEffect(() => {
    fetchCandidate();
  }, [id]);

  // ✅ SCORE SUBMIT + REDIRECT
  const submitScore = async () => {
    try {
      await API.post(
        `/candidates/${id}/scores?category=${category}&score=${score}&note=${note}`
      );

      navigate("/candidates", {
        state: { message: "Score submitted successfully 🎉" },
      });

    } catch (err) {
      setMessage("Failed to submit score");
    }
  };

  // ✅ SUMMARY + REDIRECT
  const generateSummary = async () => {
    try {
      await API.post(`/candidates/${id}/summary`);

      navigate("/candidates", {
        state: { message: "AI summary generated successfully 🤖" },
      });

    } catch (err) {
      setMessage("Failed to generate summary");
    }
  };

  if (!candidate) return <div style={{ color: "white" }}>Loading...</div>;

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2>{candidate.name}</h2>
        <p>{candidate.email}</p>
        <p>{candidate.role_applied}</p>

        {message && <p style={styles.error}>{message}</p>}

        <hr />

        <h3>AI Summary</h3>
        <p>{candidate.ai_summary || "No summary yet"}</p>

        <Button onClick={generateSummary}>
          Generate Summary
        </Button>

        <hr />

        <h3>Score Candidate</h3>

        <input
          placeholder="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={styles.input}
        />

        <input
          type="number"
          min="1"
          max="5"
          value={score}
          onChange={(e) => setScore(e.target.value)}
          style={styles.input}
        />

        <input
          placeholder="Note"
          value={note}
          onChange={(e) => setNote(e.target.value)}
          style={styles.input}
        />

        <Button onClick={submitScore}>
          Submit Score
        </Button>

        <hr />

        <h3>Scores</h3>

        {candidate.scores?.length ? (
          candidate.scores.map((s) => (
            <div key={s.id}>
              {s.category} - {s.score}/5
            </div>
          ))
        ) : (
          <p>No scores yet</p>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    padding: 30,
    background: "#0f172a",
    minHeight: "100vh",
    color: "white",
  },

  card: {
    maxWidth: 600,
    margin: "0 auto",
    background: "#1e293b",
    padding: 20,
    borderRadius: 12,
  },

  input: {
    width: "100%",
    padding: 10,
    marginBottom: 10,
    borderRadius: 6,
    border: "1px solid #333",
  },

  error: {
    color: "#22c55e",
    marginTop: 10,
  },
};