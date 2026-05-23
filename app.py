"""
NeuralSearch — Embedding-Based Semantic Search Engine
Run with: streamlit run app.py
"""

import streamlit as st
from search import SearchEngine

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuralSearch — Semantic Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load engine (cached) ──────────────────────────────────────────────────────
@st.cache_resource
def load_engine():
    return SearchEngine()

engine = load_engine()

# ── Custom CSS (preserves original design) ────────────────────────────────────
st.markdown("""
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

  .stApp {
    background: #0a0a0f !important;
    font-family: 'Syne', sans-serif;
  }

  /* Hide Streamlit chrome */
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* animated grid background */
  .stApp::before {
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

  .orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    pointer-events: none;
    z-index: 0;
    opacity: 0.15;
  }
  .orb1 { width: 600px; height: 600px; background: #6c63ff; top: -200px; left: -200px; }
  .orb2 { width: 400px; height: 400px; background: #00d4aa; bottom: -100px; right: -100px; }

  .ns-nav {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px 48px;
    border-bottom: 1px solid #1e1e2e;
  }
  .logo {
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #e8e8f0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .logo-dot { width: 8px; height: 8px; border-radius: 50%; background: #6c63ff; display: inline-block; }

  .ns-hero {
    padding: 80px 48px 40px;
    position: relative;
    z-index: 1;
    max-width: 820px;
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
  .badge-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #00d4aa;
    animation: pulse 2s infinite;
    display: inline-block;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

  .ns-hero h1 {
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -2px;
    margin-bottom: 16px;
    color: #e8e8f0;
  }
  .ns-hero h1 span { color: #6c63ff; }
  .subtitle {
    color: #6b6b80;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 500px;
    margin-bottom: 32px;
    font-family: 'DM Mono', monospace;
  }

  /* override streamlit input */
  .stTextInput input {
    background: #111118 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 18px 20px !important;
  }
  .stTextInput input:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important;
  }

  .stButton button {
    background: #6c63ff !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 10px 28px !important;
    width: 100%;
  }
  .stButton button:hover { background: #7c74ff !important; }

  .stSelectbox select, div[data-baseweb="select"] {
    background: #111118 !important;
    border: 1px solid #1e1e2e !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
  }

  .ns-stats {
    display: flex;
    gap: 32px;
    padding: 0 48px;
    margin-bottom: 32px;
    position: relative;
    z-index: 1;
  }
  .stat { display: flex; flex-direction: column; gap: 4px; }
  .stat-value {
    font-size: 1.6rem; font-weight: 800;
    letter-spacing: -1px; color: #e8e8f0;
  }
  .stat-value span { color: #6c63ff; }
  .stat-label {
    font-size: 0.75rem; color: #6b6b80;
    font-family: 'DM Mono', monospace;
    text-transform: uppercase; letter-spacing: 0.5px;
  }

  .ns-divider {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 0 48px 32px;
  }

  .result-card {
    background: #13131c;
    border: 1px solid #1e1e2e;
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
    from { opacity:0; transform: translateY(10px); }
    to   { opacity:1; transform: translateY(0); }
  }
  .result-rank {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem; color: #6b6b80;
    padding-top: 2px; min-width: 20px;
  }
  .result-body { flex: 1; }
  .result-text {
    font-size: 0.95rem; line-height: 1.6;
    color: #e8e8f0; margin-bottom: 10px;
  }
  .score-bar-wrap { display: flex; align-items: center; gap: 10px; }
  .score-bar-bg {
    flex: 1; height: 3px; background: #1e1e2e;
    border-radius: 99px; overflow: hidden;
  }
  .score-bar-fill {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, #6c63ff, #00d4aa);
  }
  .score-value {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem; color: #00d4aa;
    min-width: 42px; text-align: right;
  }
  .results-header {
    display: flex; align-items: center;
    justify-content: space-between; margin-bottom: 20px;
    padding: 0 48px;
  }
  .results-label {
    font-size: 0.75rem; font-family: 'DM Mono', monospace;
    color: #6b6b80; text-transform: uppercase; letter-spacing: 1px;
  }
  .results-count { font-size: 0.75rem; font-family: 'DM Mono', monospace; color: #00d4aa; }

  .ns-footer {
    border-top: 1px solid #1e1e2e;
    padding: 24px 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 40px;
  }
  .ns-footer span { font-size: 0.75rem; color: #6b6b80; font-family: 'DM Mono', monospace; }
  .tech-tags { display: flex; gap: 8px; }
  .tag {
    font-size: 0.7rem; font-family: 'DM Mono', monospace;
    padding: 3px 8px; border-radius: 4px;
    background: #111118; border: 1px solid #1e1e2e; color: #6b6b80;
  }
</style>
""", unsafe_allow_html=True)

# ── Nav ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="orb orb1"></div>
<div class="orb orb2"></div>
<nav class="ns-nav">
  <div class="logo"><span class="logo-dot"></span> NeuralSearch</div>
  <div style="display:flex;gap:24px">
    <a href="https://github.com/Siddhesh0024" target="_blank"
       style="color:#6b6b80;text-decoration:none;font-size:0.85rem;font-weight:600;letter-spacing:0.5px;text-transform:uppercase">GitHub</a>
  </div>
</nav>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ns-hero">
  <div class="badge"><span class="badge-dot"></span> bge-small-en · FAISS · Streamlit</div>
  <h1>Search by <span>meaning</span>,<br>not keywords.</h1>
  <p class="subtitle">Semantic search over 500K+ documents using dense vector embeddings and approximate nearest neighbor lookup.</p>
</div>
""", unsafe_allow_html=True)

# ── Search controls ───────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    query = st.text_input("", placeholder="e.g. how does vector search work?", label_visibility="collapsed")
with col2:
    top_k = st.selectbox("", [5, 10, 20], index=1, label_visibility="collapsed")
with col3:
    search_clicked = st.button("🔍 Search", use_container_width=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ns-stats">
  <div class="stat"><div class="stat-value">500<span>K+</span></div><div class="stat-label">Documents</div></div>
  <div class="stat"><div class="stat-value">384<span>d</span></div><div class="stat-label">Embedding Dim</div></div>
  <div class="stat"><div class="stat-value">29<span>%</span></div><div class="stat-label">Over TF-IDF</div></div>
  <div class="stat"><div class="stat-value">&lt;50<span>ms</span></div><div class="stat-label">Query Latency</div></div>
</div>
<hr class="ns-divider">
""", unsafe_allow_html=True)

# ── Search & Results ──────────────────────────────────────────────────────────
if search_clicked and query.strip():
    with st.spinner("Searching embeddings..."):
        results = engine.query(query.strip(), top_k=top_k)

    if not results:
        st.markdown("<p style='color:#6b6b80;font-family:DM Mono,monospace;padding:0 48px'>No results found. Try a different query.</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="results-header">
          <span class="results-label">Results</span>
          <span class="results-count">{len(results)} matches</span>
        </div>
        """, unsafe_allow_html=True)

        cards_html = '<div style="padding: 0 48px">'
        for i, r in enumerate(results):
            pct = r["score"] * 100
            cards_html += f"""
            <div class="result-card" style="animation-delay:{i*0.05}s">
              <div class="result-rank">#{i+1}</div>
              <div class="result-body">
                <div class="result-text">{r["doc"]}</div>
                <div class="score-bar-wrap">
                  <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width:{pct:.1f}%"></div>
                  </div>
                  <div class="score-value">{r["score"]:.4f}</div>
                </div>
              </div>
            </div>
            """
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

elif search_clicked and not query.strip():
    st.markdown("<p style='color:#6b6b80;font-family:DM Mono,monospace;padding:0 48px'>Please enter a search query.</p>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ns-footer">
  <span>NeuralSearch · Embedding-Based Semantic Search</span>
  <div class="tech-tags">
    <span class="tag">Python</span>
    <span class="tag">FAISS</span>
    <span class="tag">sentence-transformers</span>
    <span class="tag">Streamlit</span>
  </div>
</div>
""", unsafe_allow_html=True)