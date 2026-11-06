import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = "https://resume-iq-n7va.onrender.com";

function App() {
  const [file, setFile] = useState(null);
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_BASE}/history`);
      setHistory(res.data);
    } catch (err) {
      console.error("Error fetching history:", err);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!file || !jobDescription) {
      alert("Please upload a PDF resume and provide a Job Description.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_title", jobTitle || "Target Role");
    formData.append("job_description", jobDescription);

    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResult(res.data);
      fetchHistory();
    } catch (err) {
      alert(err.response?.data?.detail || "An error occurred during analysis.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>ResumeIQ</h1>
        <p>AI-Powered Resume Intelligence & Job Matching System</p>
      </header>

      <div className="grid">
        {/* Input Form */}
        <div className="card">
          <h2>Upload & Analyze</h2>
          <form onSubmit={handleAnalyze}>
            <div className="form-group">
              <label>Target Job Title</label>
              <input 
                type="text" 
                placeholder="e.g. Backend Developer" 
                value={jobTitle} 
                onChange={(e) => setJobTitle(e.target.value)} 
              />
            </div>

            <div className="form-group">
              <label>Upload PDF Resume</label>
              <input 
                type="file" 
                accept=".pdf" 
                onChange={(e) => setFile(e.target.files[0])} 
              />
            </div>

            <div className="form-group">
              <label>Job Description</label>
              <textarea 
                rows="6" 
                placeholder="Paste the job description here..." 
                value={jobDescription} 
                onChange={(e) => setJobDescription(e.target.value)} 
              />
            </div>

            <button type="submit" disabled={loading}>
              {loading ? "Analyzing via Local NLP..." : "Analyze Match"}
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div className="card">
          <h2>Analysis Output</h2>
          {result ? (
            <div>
              <div className="score-box">
                <div>Overall Compatibility Score</div>
                <div className="score-circle">{result.overall_score}%</div>
                <small>TF-IDF Match: {result.tfidf_score}% | Semantic Match: {result.semantic_score}%</small>
              </div>

              <h3>Matched Skills</h3>
              <div className="skills-list">
                {result.matched_skills.map((s, i) => (
                  <span key={i} className="badge badge-success">{s}</span>
                ))}
              </div>

              <h3>Missing / Gap Skills</h3>
              <div className="skills-list">
                {result.missing_skills.map((s, i) => (
                  <span key={i} className="badge badge-danger">{s}</span>
                ))}
              </div>

              <h3>Actionable AI Insights</h3>
              <ul>
                {result.recommendations.map((rec, i) => (
                  <li key={i}>{rec}</li>
                ))}
              </ul>
            </div>
          ) : (
            <p style={{ color: "var(--text-muted)" }}>Fill in the form on the left to see instant score visualizations, skill gap analysis, and AI insights.</p>
          )}
        </div>
      </div>

      {/* History Section */}
      <div className="card" style={{ marginTop: "2rem" }}>
        <h2>Analysis History (PostgreSQL / DB)</h2>
        {history.length === 0 ? <p>No previous analyses found.</p> : (
          history.map((item) => (
            <div className="history-item" key={item.id}>
              <div>
                <strong>{item.job_title}</strong> ({item.filename})
                <br />
                <small style={{ color: "var(--text-muted)" }}>{item.created_at}</small>
              </div>
              <div style={{ fontSize: "1.2rem", fontWeight: "bold", color: "#38bdf8" }}>
                {item.overall_score}% Match
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;