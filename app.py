import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0b0b12;
    background-image: 
        radial-gradient(ellipse 70% 50% at 15% 5%, rgba(255, 140, 50, 0.08) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 85% 95%, rgba(255, 80, 30, 0.05) 0%, transparent 50%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(255, 140, 50, 0.02) 0%, transparent 70%);
    min-height: 100vh;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 3rem;
    max-width: 1300px;
    margin: 0 auto;
}

/* ── Scrollbar ── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.02);
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 140, 50, 0.3);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 140, 50, 0.5);
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(255, 140, 50, 0.1);
    border: 1px solid rgba(255, 140, 50, 0.15);
    border-radius: 100px;
    padding: 0.35rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}
.hero h1 {
    font-family: 'Inter', sans-serif;
    font-size: clamp(3.2rem, 7vw, 5.5rem);
    font-weight: 900;
    line-height: 1.0;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #f0ebe0 0%, #ff8c32 70%, #ff5a1a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.8rem;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #908880;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.7;
    letter-spacing: 0.01em;
}
.hero-sub strong {
    color: #ff8c32;
    font-weight: 500;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 140, 50, 0.2), rgba(255, 140, 50, 0.4), rgba(255, 140, 50, 0.2), transparent);
    margin: 2rem 0 2.5rem;
}

/* ── Input card ── */
.input-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
    transition: border-color 0.3s, box-shadow 0.3s;
}
.input-card:hover {
    border-color: rgba(255, 140, 50, 0.15);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    color: #f0ebe0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1.2rem !important;
    transition: all 0.3s !important;
}
.stTextInput > div > div > input::placeholder {
    color: #504840 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 4px rgba(255, 140, 50, 0.08), 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    background: rgba(255, 255, 255, 0.05) !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0b0b12 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2.5rem !important;
    cursor: pointer !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 24px rgba(255, 140, 50, 0.25) !important;
    width: 100%;
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
    transition: left 0.6s;
}
.stButton > button:hover::before {
    left: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(255, 140, 50, 0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 12px rgba(255, 140, 50, 0.2) !important;
}

/* ── Example chips ── */
.chip-container {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    align-items: center;
    margin-top: 0.5rem;
}
.chip-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #605850;
    letter-spacing: 0.1em;
    margin-right: 0.3rem;
}
.chip {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 0.35rem 1rem;
    font-size: 0.75rem;
    color: #a09890;
    font-family: 'Inter', sans-serif;
    cursor: default;
    transition: all 0.2s;
    user-select: none;
}
.chip:hover {
    background: rgba(255, 140, 50, 0.08);
    border-color: rgba(255, 140, 50, 0.2);
    color: #f0ebe0;
    transform: translateY(-1px);
}

/* ── Pipeline section ── */
.pipeline-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}
.section-heading {
    font-family: 'Inter', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #f0ebe0;
    letter-spacing: -0.01em;
}
.pipeline-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #605850;
    letter-spacing: 0.1em;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.step-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255, 140, 50, 0.03), transparent);
    opacity: 0;
    transition: opacity 0.4s;
}
.step-card:hover::after {
    opacity: 1;
}
.step-card.active {
    border-color: rgba(255, 140, 50, 0.3);
    background: rgba(255, 140, 50, 0.05);
    box-shadow: 0 4px 24px rgba(255, 140, 50, 0.05);
}
.step-card.done {
    border-color: rgba(80, 200, 120, 0.2);
    background: rgba(80, 200, 120, 0.03);
}
.step-card .step-indicator {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    border-radius: 0 3px 3px 0;
    background: rgba(255, 255, 255, 0.05);
    transition: background 0.4s;
}
.step-card.active .step-indicator { background: #ff8c32; }
.step-card.done .step-indicator { background: #50c878; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    position: relative;
    z-index: 1;
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    color: #ff8c32;
    opacity: 0.6;
    background: rgba(255, 140, 50, 0.08);
    padding: 0.1rem 0.6rem;
    border-radius: 4px;
}
.step-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #f0ebe0;
    flex: 1;
}
.step-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.8rem;
    border-radius: 100px;
    font-weight: 500;
}
.status-waiting {
    color: #504840;
    background: rgba(255, 255, 255, 0.03);
}
.status-running {
    color: #ff8c32;
    background: rgba(255, 140, 50, 0.1);
    animation: pulse-status 1.5s ease-in-out infinite;
}
.status-done {
    color: #50c878;
    background: rgba(80, 200, 120, 0.08);
}
.step-desc {
    font-size: 0.78rem;
    color: #706860;
    margin-top: 0.3rem;
    padding-left: 2.4rem;
    position: relative;
    z-index: 1;
}

@keyframes pulse-status {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* ── Result panels ── */
.result-panel {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-top: 0.8rem;
    margin-bottom: 1.2rem;
}
.result-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255, 140, 50, 0.08);
}
.result-content {
    font-size: 0.9rem;
    line-height: 1.8;
    color: #cdc8bf;
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: linear-gradient(135deg, rgba(255, 140, 50, 0.03), rgba(255, 140, 50, 0.01));
    border: 1px solid rgba(255, 140, 50, 0.15);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}
.report-panel::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 40%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(255, 140, 50, 0.03), transparent 70%);
    pointer-events: none;
}
.feedback-panel {
    background: linear-gradient(135deg, rgba(80, 200, 120, 0.03), rgba(80, 200, 120, 0.01));
    border: 1px solid rgba(80, 200, 120, 0.15);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-top: 1.5rem;
}
.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.panel-label.orange {
    color: #ff8c32;
    border-bottom: 1px solid rgba(255, 140, 50, 0.1);
}
.panel-label.green {
    color: #50c878;
    border-bottom: 1px solid rgba(80, 200, 120, 0.1);
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    color: #908880 !important;
    letter-spacing: 0.05em !important;
    background: rgba(255, 255, 255, 0.02) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
}
.streamlit-expanderHeader:hover {
    background: rgba(255, 255, 255, 0.04) !important;
    border-color: rgba(255, 140, 50, 0.1) !important;
}
.streamlit-expanderContent {
    background: transparent !important;
}

/* ── Download button ── */
.download-btn {
    margin-top: 1.2rem;
}
.download-btn .stButton > button {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #f0ebe0 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: none !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.85rem !important;
    width: auto !important;
}
.download-btn .stButton > button:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 140, 50, 0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Footer ── */
.footer {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #403830;
    text-align: center;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.03);
    letter-spacing: 0.08em;
}
.footer span {
    color: #ff8c32;
}

/* ── Toast/Warning ── */
.stAlert {
    background: rgba(255, 140, 50, 0.05) !important;
    border: 1px solid rgba(255, 140, 50, 0.15) !important;
    border-radius: 12px !important;
    color: #f0ebe0 !important;
    font-family: 'Inter', sans-serif !important;
}
.stAlert svg {
    fill: #ff8c32 !important;
}

/* ── Spinner ── */
.stSpinner > div {
    color: #ff8c32 !important;
    border-color: #ff8c32 !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1.2rem 2rem;
    }
    .input-card {
        padding: 1.5rem;
    }
    .report-panel {
        padding: 1.5rem;
    }
    .feedback-panel {
        padding: 1.5rem;
    }
    .step-card {
        padding: 1rem 1.2rem;
    }
    .hero h1 {
        font-size: 2.8rem;
    }
}

/* ── Fix for module loading issue ── */
.stTextInput > div {
    position: relative;
}
.stTextInput > div > div {
    position: relative;
}
</style>
""",
    unsafe_allow_html=True,
)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done": ("✓ DONE", "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(
        f"""
    <div class="step-card {card_cls}">
        <div class="step-indicator"></div>
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div class='step-desc'>" + desc + "</div>" if desc else ""}
    </div>
    """,
        unsafe_allow_html=True,
    )


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
    <div class="hero-badge">✦ Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — <strong>searching</strong>, <strong>scraping</strong>,
        <strong>writing</strong>, and <strong>critiquing</strong> — to deliver a polished research report.
    </p>
</div>
<div class="divider"></div>
""",
    unsafe_allow_html=True,
)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    # Use a container for the input to avoid module loading issues
    with st.container():
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025",
            key="topic_input",
            label_visibility="visible",
        )

    run_btn = st.button("⚡ Run Research Pipeline", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Example chips
    st.markdown(
        """
    <div class="chip-container">
        <span class="chip-label">TRY →</span>
    """,
        unsafe_allow_html=True,
    )
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f'<span class="chip">{ex}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown(
        """
    <div class="pipeline-header">
        <div class="section-heading">⚙️ Pipeline</div>
        <div class="pipeline-status">4 STEPS</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        if step in r:
            return "done"
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent", s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent", s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain", s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain", s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍 Search Agent is gathering information…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Find recent, reliable and detailed information about: {topic_val}",
                    )
                ]
            }
        )
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None

    # ── Step 2: Reader ──
    with st.spinner("📄 Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic_val}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{results['search'][:800]}",
                    )
                ]
            }
        )
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️ Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke(
            {"topic": topic_val, "research": research_combined}
        )
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐 Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📊 Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div></div>',
                unsafe_allow_html=True,
            )

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div></div>',
                unsafe_allow_html=True,
            )

    # Final report
    if "writer" in r:
        st.markdown(
            """
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.markdown('<div class="download-btn">', unsafe_allow_html=True)
        st.download_button(
            label="⬇ Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Critic feedback
    if "critic" in r:
        st.markdown(
            """
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="footer">
    ResearchMind · Powered by <span>LangChain</span> multi-agent pipeline · Built with <span>Streamlit</span>
</div>
""",
    unsafe_allow_html=True,
)
