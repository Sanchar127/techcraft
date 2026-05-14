import React from "react";
import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Candidates from "./pages/Candidates";
import CandidateDetail from "./pages/CandidateDetail";
import EditCandidate from "./pages/EditCandidate"; 
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/candidates" element={<Candidates />} />
      <Route path="/candidates/:id" element={<CandidateDetail />} />

      {/* ✅ THIS FIXES YOUR BLANK PAGE */}
      <Route path="/edit/:id" element={<EditCandidate />} />
    </Routes>
  );
}