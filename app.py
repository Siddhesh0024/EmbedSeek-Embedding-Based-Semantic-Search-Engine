from flask import Flask, request, jsonify, render_template_string
from search import SearchEngine

app = Flask(__name__)
engine = SearchEngine()

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NeuralSearch — Semantic Search Engine</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --accent: #6c63ff;
    --accent2: #00d4aa;
    --text: #e8e8f0;
    --muted: #6b6b80;
    --card: #13131c;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Syne', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* animated grid background */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(108,99,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(108,99,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  /* glow orbs */
  .orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    pointer-events: none;
    z-index: 0;
    opacity: 0.15;
  }
  .orb1 { width: 600px; height: 600px; background: var(--accent); top: -200px; left: -200px; }
  .orb2 { width: 400px; height: 400px; background: var(--accent2); bottom: -100px; right: -100px; }

  .container {
    position: relative;
    z-index: 1;
    max-width: 820px;
    margin: 0 auto;
    padding: 0 24px;
  }

  /* NAV */
  nav {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px 48px;
    border-bottom: 1px solid var(--border);
  }
  .logo {
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .logo-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); display: inline-block; }
  .nav-links { display: flex; gap: 24px; }
  .nav-links a {
    color: var(--muted);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    transition: color 0.2s;
  }
  .nav-links a:hover { color: var(--text); }

  /* HERO */
  .hero {
    padding: 80px 48px 60px;
    position: relative;
    z-index: 1;
  }
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(108,99,255,0.1);
    border: 1px solid rgba(108,99,255,0.3);
    color: #a89fff;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    padding: 4px 12px;
    border-radius: 100px;
    margin-bottom: 28px;
    letter-spacing: 0.5px;
  }
  .badge-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent2); animation: pulse 2s infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

  h1 {
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -2px;
    margin-bottom: 16px;
  }
  h1 span { color: var(--accent); }

  .subtitle {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.6;
    max-width: 500px;
    margin-bottom: 48px;
    font-family: 'DM Mono', monospace;
  }

  /* SEARCH BOX */
  .search-wrap {
    position: relative;
    margin-bottom: 16px;
  }
  .search-wrap input[type="text"] {
    width: 100%;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 140px 18px 20px;
    color: var(--text);
    font-family: 'DM Mono', monospace;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .search-wrap input[type="text"]:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15);
  }
  .search-wrap input[type="text"]::placeholder { color: var(--muted); }

  .search-btn {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
    letter-spacing: 0.3px;
  }
  .search-btn:hover { background: #7c74ff; }
  .search-btn:active { transform: translateY(-50%) scale(0.97); }
  .search-btn:disabled { opacity: 0.5; cursor: not-allowed; }

  .options-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 48px;
  }
  .options-row label {
    color: var(--muted);
    font-size: 0.8rem;
    font-family: 'DM Mono', monospace;
  }
  .options-row select {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    padding: 6px 10px;
    border-radius: 6px;
    outline: none;
    cursor: pointer;
  }

  /* STATS */
  .stats {
    display: flex;
    gap: 32px;
    padding: 0 48px;
    margin-bottom: 48px;
    position: relative;
    z-index: 1;
  }
  .stat {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .stat-value {
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: var(--text);
  }
  .stat-value span { color: var(--accent); }
  .stat-label {
    font-size: 0.75rem;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* DIVIDER */
  .divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 0 48px 48px;
    position: relative;
    z-index: 1;
  }

  /* RESULTS */
  .results-section {
    padding: 0 48px 80px;
    position: relative;
    z-index: 1;
  }
  .results-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  .results-label {
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .results-count {
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    color: var(--accent2);
  }

  .result-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
    display: flex;
    gap: 20px;
    align-items: flex-start;
    transition: border-color 0.2s, transform 0.2s;
    animation: fadeUp 0.3s ease both;
  }
  .result-card:hover {
    border-color: rgba(108,99,255,0.4);
    transform: translateX(4px);
  }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .result-rank {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    padding-top: 2px;
    min-width: 20px;
  }

  .result-body { flex: 1; }

  .result-text {
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text);
    margin-bottom: 10px;
    font-weight: 400;
  }

  .score-bar-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .score-bar-bg {
    flex: 1;
    height: 3px;
    background: var(--border);
    border-radius: 99px;
    overflow: hidden;
  }
  .score-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 0.6s ease;
  }
  .score-value {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--accent2);
    min-width: 42px;
    text-align: right;
  }

  /* LOADING */
  .loading {
    display: none;
    align-items: center;
    gap: 10px;
    padding: 0 48px;
    margin-bottom: 24px;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: var(--muted);
    position: relative;
    z-index: 1;
  }
  .spinner {
    width: 16px; height: 16px;
    border: 2px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* EMPTY */
  .empty {
    text-align: center;
    padding: 60px 0;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    display: none;
  }

  /* FOOTER */
  footer {
    position: relative;
    z-index: 1;
    border-top: 1px solid var(--border);
    padding: 24px 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  footer span {
    font-size: 0.75rem;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
  }
  .tech-tags { display: flex; gap: 8px; }
  .tag {
    font-size: 0.7rem;
    font-family: 'DM Mono', monospace;
    padding: 3px 8px;
    border-radius: 4px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
  }
</style>
</head>
<body>

<div class="orb orb1"></div>
<div class="orb orb2"></div>

<nav>
  <div class="logo">
    <span class="logo-dot"></span>
    NeuralSearch
  </div>
  <div class="nav-links">
    <a href="https://github.com" target="_blank">GitHub</a>
    <a href="#" onclick="showDocs()">API Docs</a>
  </div>
</nav>

<div class="hero">
  <div class="badge"><span class="badge-dot"></span> bge-small-en · FAISS · Flask</div>
  <h1>Search by <span>meaning</span>,<br>not keywords.</h1>
  <p class="subtitle">Semantic search over 500K+ documents using dense vector embeddings and approximate nearest neighbor lookup.</p>

  <div class="search-wrap">
    <input type="text" id="queryInput" placeholder="e.g. how does vector search work?" />
    <button class="search-btn" id="searchBtn" onclick="doSearch()">Search</button>
  </div>

  <div class="options-row">
    <label>Results:</label>
    <select id="topK">
      <option value="5">5</option>
      <option value="10" selected>10</option>
      <option value="20">20</option>
    </select>
  </div>
</div>

<div class="stats">
  <div class="stat">
    <div class="stat-value">500<span>K+</span></div>
    <div class="stat-label">Documents</div>
  </div>
  <div class="stat">
    <div class="stat-value">384<span>d</span></div>
    <div class="stat-label">Embedding Dim</div>
  </div>
  <div class="stat">
    <div class="stat-value">29<span>%</span></div>
    <div class="stat-label">Over TF-IDF</div>
  </div>
  <div class="stat">
    <div class="stat-value">&lt;50<span>ms</span></div>
    <div class="stat-label">Query Latency</div>
  </div>
</div>

<hr class="divider">

<div class="loading" id="loading">
  <div class="spinner"></div>
  Searching embeddings...
</div>

<div class="results-section" id="resultsSection" style="display:none">
  <div class="results-header">
    <span class="results-label">Results</span>
    <span class="results-count" id="resultsCount"></span>
  </div>
  <div id="resultsList"></div>
</div>

<div class="empty" id="emptyState">No results found. Try a different query.</div>

<footer>
  <span>NeuralSearch · Embedding-Based Semantic Search</span>
  <div class="tech-tags">
    <span class="tag">Python</span>
    <span class="tag">FAISS</span>
    <span class="tag">sentence-transformers</span>
    <span class="tag">Flask</span>
  </div>
</footer>

<script>
  document.getElementById("queryInput").addEventListener("keydown", e => {
    if (e.key === "Enter") doSearch();
  });

  async function doSearch() {
    const query = document.getElementById("queryInput").value.trim();
    const top_k = parseInt(document.getElementById("topK").value);
    if (!query) return;

    const btn = document.getElementById("searchBtn");
    btn.disabled = true;
    document.getElementById("loading").style.display = "flex";
    document.getElementById("resultsSection").style.display = "none";
    document.getElementById("emptyState").style.display = "none";

    try {
      const res = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k })
      });
      const data = await res.json();

      document.getElementById("loading").style.display = "none";
      btn.disabled = false;

      if (!data.length) {
        document.getElementById("emptyState").style.display = "block";
        return;
      }

      document.getElementById("resultsCount").textContent = `${data.length} matches`;
      const list = document.getElementById("resultsList");
      list.innerHTML = "";

      data.forEach((r, i) => {
        const pct = (r.score * 100).toFixed(1);
        const card = document.createElement("div");
        card.className = "result-card";
        card.style.animationDelay = `${i * 0.05}s`;
        card.innerHTML = `
          <div class="result-rank">#${i+1}</div>
          <div class="result-body">
            <div class="result-text">${r.doc}</div>
            <div class="score-bar-wrap">
              <div class="score-bar-bg">
                <div class="score-bar-fill" style="width:${pct}%"></div>
              </div>
              <div class="score-value">${r.score.toFixed(4)}</div>
            </div>
          </div>
        `;
        list.appendChild(card);
      });

      document.getElementById("resultsSection").style.display = "block";
    } catch(e) {
      document.getElementById("loading").style.display = "none";
      btn.disabled = false;
      alert("Search failed. Make sure the server is running.");
    }
  }

  function showDocs() {
    alert("POST /search\\n\\nBody: { \\"query\\": \\"your text\\", \\"top_k\\": 10 }\\n\\nReturns: [{ doc, score }]");
  }
</script>
</body>
</html>'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    results = engine.query(data["query"], top_k=data.get("top_k", 10))
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)