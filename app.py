import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from analyzer import parse_script_into_beats, calculate_tension_curve, detect_optimal_cliffhangers, generate_hook_rewrite
from sample_scripts import SAMPLE_SCRIPTS

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="HookGenius | Kuku TV Retention Calibrator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom Styling (Kuku TV Dark Aesthetic) -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main {
        background-color: #0b0f19;
    }
    
    /* Header Styles */
    .kuku-badge {
        display: inline-block;
        background: linear-gradient(135deg, #e11d48 0%, #be123c 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .hero-title {
        font-size: 30px;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    
    .hero-sub {
        font-size: 13px;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #131b2e;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    
    .metric-val {
        font-size: 22px;
        font-weight: 800;
        color: #f43f5e;
    }
    
    .metric-label {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Cut Point Cards */
    .cut-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-left: 4px solid #f43f5e;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
        transition: transform 0.15s ease;
    }
    .cut-card:hover {
        border-color: #f43f5e;
        transform: translateY(-2px);
    }
    
    .cut-title {
        font-size: 14px;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .cut-quote {
        background: #0f172a;
        border-radius: 6px;
        padding: 10px;
        font-family: monospace;
        font-size: 12px;
        color: #cbd5e1;
        margin: 8px 0;
        border-left: 2px solid #38bdf8;
    }
    
    .badge-unlock {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }
    
    .badge-trigger {
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.3);
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Sidebar Navigation -----------------
with st.sidebar:
    st.markdown('<div class="kuku-badge">⚡ Kuku AI Labs Prototype</div>', unsafe_allow_html=True)
    st.markdown("### 🎬 Script Ingestion")
    
    script_mode = st.radio(
        "Choose Script Source:",
        ["Sample Indian Micro-Dramas", "Paste Custom Screenplay"],
        index=0
    )
    
    if script_mode == "Sample Indian Micro-Dramas":
        selected_title = st.selectbox(
            "Select Drama Genre:",
            list(SAMPLE_SCRIPTS.keys()),
            index=0
        )
        active_script = SAMPLE_SCRIPTS[selected_title]
    else:
        active_script = st.text_area(
            "Paste Screenplay Text:",
            height=300,
            value=SAMPLE_SCRIPTS["The Secret Heir's Revenge (Billionaire Drama)"]
        )

    st.markdown("---")
    st.markdown("### 🎯 Kuku Business Levers")
    st.caption("**Primary Metric:** Episode 1 ➔ Episode 2 Coin-Unlock Rate")
    st.caption("**Target Platform:** Kuku TV Vertical Dramas & Kuku FM Series")
    st.caption("**Engine:** 1st-Principles Narrative Pacing & Tension Heuristics")

# ----------------- Header Banner -----------------
st.markdown('<div class="kuku-badge">Content Ops & Retention Engineering</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">HookGenius: Micro-Drama Retention Calibrator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Automatically mapping narrative tension curves and identifying optimal cliffhanger moments to maximize coin-unlock retention.</div>',
    unsafe_allow_html=True
)

# ----------------- Processing Pipeline -----------------
beats = parse_script_into_beats(active_script)
scored_beats = calculate_tension_curve(beats)
cliffhangers = detect_optimal_cliffhangers(scored_beats)

# Calculate Macro Metrics
avg_tension = sum(b["smoothed_tension"] for b in scored_beats) / max(1, len(scored_beats))
peak_tension = max((b["smoothed_tension"] for b in scored_beats), default=0)
top_unlock_prob = cliffhangers[0]["coin_unlock_prob"] if cliffhangers else 75.0

# ----------------- KPI Cards Row -----------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val">{round(top_unlock_prob)}%</div>
        <div class="metric-label">Max Coin-Unlock Potential</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val" style="color:#38bdf8;">{round(peak_tension)}/100</div>
        <div class="metric-label">Peak Narrative Tension</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val" style="color:#34d399;">{len(cliffhangers)} Cut Points</div>
        <div class="metric-label">Identified Binge Hooks</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    grade = "A+ (Binge Magnet)" if top_unlock_prob > 90 else ("A (High Retention)" if top_unlock_prob > 80 else "B (Needs Punching Up)")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val" style="color:#fbbf24;">{grade.split()[0]}</div>
        <div class="metric-label">Retention Grade: {grade.split('(')[1].replace(')', '')}</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- Main Visualization: Interactive Tension Wave -----------------
st.markdown("### 📈 Real-Time Narrative Tension Wave")
st.caption("Visualizing beat-by-beat emotional arousal, dialogue velocity, and conflict density across scenes.")

df = pd.DataFrame(scored_beats)
fig = go.Figure()

# Plot smoothed tension curve
fig.add_trace(go.Scatter(
    x=df["index"],
    y=df["smoothed_tension"],
    mode="lines",
    name="Emotional Tension",
    line=dict(color="#f43f5e", width=3, shape="spline"),
    fill="tozeroy",
    fillcolor="rgba(244, 63, 94, 0.12)",
    hovertemplate="<b>Beat %{x}</b><br>Tension: %{y}/100<extra></extra>"
))

# Highlight Cliffhanger Cut Points with vertical reference lines & markers
for idx, cut in enumerate(cliffhangers):
    fig.add_vline(
        x=cut["beat_index"],
        line_width=2,
        line_dash="dash",
        line_color="#38bdf8" if idx == 0 else "#94a3b8",
        annotation_text=f"Cut #{idx+1} ({cut['coin_unlock_prob']}%)",
        annotation_position="top left",
        annotation_font=dict(size=10, color="#ffffff")
    )

fig.update_layout(
    height=340,
    margin=dict(l=10, r=10, t=30, b=10),
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    xaxis=dict(
        title="Narrative Beat / Scene Progression",
        gridcolor="#1e293b",
        color="#94a3b8"
    ),
    yaxis=dict(
        title="Tension Score (0 - 100)",
        gridcolor="#1e293b",
        color="#94a3b8",
        range=[10, 105]
    ),
    hovermode="x unified",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ----------------- Bottom Section: Cut Recommendations & Hook Doctor -----------------
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### ✂️ Top Episode Cut Recommendations")
    st.caption("Mathematically optimal lines to roll credits on, forcing the viewer to unlock Episode 2.")
    
    for i, cut in enumerate(cliffhangers):
        badge_label = "🏆 Recommended Cut" if i == 0 else f"Alternative Option #{i+1}"
        st.markdown(f"""
        <div class="cut-card">
            <div class="cut-title">
                <span>{badge_label} • {cut['scene']}</span>
                <span class="badge-unlock">💰 {cut['coin_unlock_prob']}% Coin-Unlock Prob</span>
            </div>
            <div class="cut-quote">
                <b>{cut['character']}:</b> "{cut['line']}"
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
                <span class="badge-trigger">⚡ {cut['trigger_type']}</span>
                <span style="font-size:11px; color:#94a3b8;"><b>Why it hooks:</b> {cut['rationale']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 🩺 Hook Doctor (Rewrite Assistant)")
    st.caption("AI-powered punch-up for scenes ending on low energy.")
    
    # Pick a scene beat that could be punched up
    sample_weak = scored_beats[min(4, len(scored_beats)-1)]
    rewrite = generate_hook_rewrite(sample_weak)
    
    st.markdown("**Original Underwhelming Line:**")
    st.code(sample_weak["text"], language="markdown")
    
    st.markdown(f"**⚡ High-Retention Punch-Up ({rewrite['retention_boost']}):**")
    st.code(rewrite["improved"], language="markdown")
    
    st.info(
        "💡 **Kuku Content Rule:** Micro-drama episodes must never end on emotional resolution. "
        "Always cut on an unanswered revelation, sudden physical threat, or financial inversion."
    )
    
    # Export Options
    st.markdown("### 📥 Content Greenlight Export")
    export_summary = f"""# HookGenius Analysis Report
Drama Title: Selected Script
Peak Narrative Tension: {round(peak_tension)}/100
Maximum Coin-Unlock Potential: {round(top_unlock_prob)}%
Recommended Cut Line: {cliffhangers[0]['line'] if cliffhangers else 'N/A'}
Trigger Type: {cliffhangers[0]['trigger_type'] if cliffhangers else 'N/A'}
"""
    st.download_button(
        label="📄 Download Executive Coverage Report (MD)",
        data=export_summary,
        file_name="hookgenius_coverage_report.md",
        mime="text/markdown",
        use_container_width=True
    )
