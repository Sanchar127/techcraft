import { useState } from "react";
import API from "../api/client";
import Button from "./Button";

export default function ScoreForm({ candidateId }) {
  const [category, setCategory] = useState("");
  const [score, setScore] = useState(3);
  const [note, setNote] = useState("");

  const submit = async () => {
    await API.post(`/candidates/${candidateId}/scores`, null, {
      params: { category, score, note }
    });

    alert("Score submitted");
  };

  return (
    <div>
      <h3>Score Candidate</h3>

      <input placeholder="category" onChange={(e) => setCategory(e.target.value)} />
      <input
        type="number"
        value={score}
        onChange={(e) => setScore(e.target.value)}
      />
      <input placeholder="note" onChange={(e) => setNote(e.target.value)} />

      <Button onClick={submit}>Submit Score</Button>
    </div>
  );
}