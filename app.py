import streamlit as st
import tempfile
import json
import os
import pandas as pd
from document_agent import DocumentProcessingAgent

# Page Configuration
st.set_page_config(
    page_title="StudyLens AI — Document Processing Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-Tier Custom UI Styling & Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Gradient Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(20, 24, 40, 0.95) 0%, rgba(10, 12, 22, 0.98) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 20px;
        padding: 2.2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 35px -10px rgba(99, 102, 241, 0.25);
        animation: fadeIn 0.8s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid #6366f1;
        color: #a5b4fc;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 70%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.2;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 0.6rem;
        font-weight: 400;
    }

    /* Metric Cards with Neon Hover */
    .metric-card {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 1.5rem 1.2rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.25);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }

    /* Animation Keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Code & JSON styling */
    pre, code {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.88rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Header Section ---
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ StudyLens AI Pipeline • Agentic Architecture</div>
    <div class="hero-title">Document Processing Agent</div>
    <div class="hero-subtitle">High-fidelity text extraction, structural noise reduction, and semantic chunking engine.</div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Controls ---
with st.sidebar:
    st.markdown("### ⚙️ Engine Parameters")
    st.caption("Tune chunking configuration for optimal RAG context windows.")
    
    chunk_size = st.slider(
        "Chunk Window Size",
        min_value=300,
        max_value=2500,
        value=1000,
        step=50,
        help="Target length of each text segment."
    )
    
    chunk_overlap = st.slider(
        "Inter-Chunk Overlap",
        min_value=50,
        max_value=500,
        value=150,
        step=25,
        help="Characters preserved across boundaries to retain semantic context."
    )
    
    st.markdown("---")
    st.markdown("""
    <div style='background: rgba(255,255,255,0.03); border-radius: 12px; padding: 1rem; border: 1px solid rgba(255,255,255,0.06); font-size: 0.85rem; color: #94a3b8;'>
        <b style='color:#e2e8f0;'>Integration Flow:</b><br>
        1. Parse & clean raw PDF<br>
        2. Generate semantic chunks<br>
        3. Pass payload to <b>Tutor & Question Agents</b>
    </div>
    """, unsafe_allow_html=True)

agent = DocumentProcessingAgent(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

# --- Document Upload Field ---
uploaded_file = st.file_uploader(
    "Select Study Material (Textbook, Lecture Slides, or Notes in PDF)",
    type=["pdf"],
    help="Upload PDF to trigger autonomous extraction and chunking."
)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    with st.spinner("Processing document... Extracting structural layers..."):
        result = agent.process_document(tmp_file_path)

    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)

    if result["status"] == "success":
        # Animated High-Aesthetic Metrics
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{result['total_pages']}</div>
                <div class="metric-label">Document Pages</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{result['total_characters']:,}</div>
                <div class="metric-label">Characters Parsed</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{result['total_chunks']}</div>
                <div class="metric-label">Semantic Chunks</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            avg_len = int(result['total_characters'] / result['total_chunks']) if result['total_chunks'] > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_len}</div>
                <div class="metric-label">Avg Characters / Chunk</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        # Content Inspection Tabs
        tab1, tab2, tab3 = st.tabs([
            "🧩 Semantic Chunks",
            "📜 Normalized Corpus",
            "⚡ Downstream Handoff Payload"
        ])

        with tab1:
            st.markdown(f"#### Structured Chunk Sequences (`Total: {result['total_chunks']}`)")
            for chunk in result["chunks"]:
                with st.expander(f"🔹 Chunk #{chunk['chunk_id']} — Page {chunk['page']} ({chunk['char_length']} chars)"):
                    st.code(chunk["text"], language="text")

        with tab2:
            st.markdown("#### Full Normalized Text View")
            st.text_area(
                "Complete Text Stream",
                result["full_text"],
                height=400,
                help="Cleaned representation with stripped headers and unified line boundaries."
            )

        with tab3:
            st.markdown("#### Autonomous Multi-Agent Handshake")
            st.caption("Standardized schema ready for Tutor, Question Generator, and Orchestrator Agents.")

            payload_json = json.dumps(result, indent=4)
            st.download_button(
                label="💾 Download Verified Payload (JSON)",
                data=payload_json,
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}_processed.json",
                mime="application/json",
                use_container_width=True
            )
            st.write("")
            st.json(result)

    else:
        st.error(f"Execution Error: {result.get('message', 'Failed to process document')}")