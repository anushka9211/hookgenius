import time
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from analyzer import (
    parse_script_into_beats,
    calculate_tension_curve,
    detect_optimal_cliffhangers,
    generate_ab_test_rewrites,
    compute_telemetry,
    export_normalized_analytics_dataset
)
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
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    
    .hero-sub {
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 18px;
    }
    
    .metric-card {
        background: #131b2e;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    
    .metric-val {
        font-size: 20px;
        font-weight: 800;
        color: #f43f5e;
    }
    
    .metric-label {
        font-size: 10px;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .cut-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-left: 4px solid #f43f5e;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 12px;
    }
    
    .cut-title {
        font-size: 13px;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .cut-quote {
        background: #0f172a;
        border-radius: 6px;
        padding: 8px 10px;
        font-family: monospace;
        font-size: 11px;
        color: #cbd5e1;
        margin: 8px 0;
        border-left: 2px solid #38bdf8;
    }
    
    .badge-index {
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.35);
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }
    
    .telemetry-box {
        background: #080c14;
        border: 1px dashed #334155;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 11px;
        color: #94a3b8;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Start execution timer for telemetry
pipeline_start_time = time.time()

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
            height=280,
            value=SAMPLE_SCRIPTS["The Secret Heir's Revenge (Billionaire Drama)"]
        )

    st.markdown("---")
    st.markdown("### ⚙️ Production Telemetry")
    telemetry = compute_telemetry(active_script, pipeline_start_time)
    
    st.markdown(f"""
    <div class="telemetry-box">
        <div><b>Tokens Ingested:</b> ~{telemetry['est_tokens']:,}</div>
        <div><b>Est. Inference Cost:</b> {telemetry['cost_inr']}</div>
        <div><b>Execution Latency:</b> {telemetry['latency_sec']}</div>
        <div style="font-size:9px; color:#64748b; margin-top:4px;">*Benchmarked on Gemini 3.8 Flash unit economics.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Kuku Business Levers")
    st.caption("**Core Metric:** Ep 1 ➔ Ep 2 Coin-Unlock Retention")
    st.caption("**Target Platform:** Kuku TV Vertical Dramas & Kuku FM Series")
    st.caption("**Methodology:** Interpretable Heuristic Rubric (Not ungrounded ML probabilities)")

# ----------------- Header Banner -----------------
st.markdown('<div class="kuku-badge">Content Operations & Retention Strategy</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">HookGenius: Micro-Drama Retention Calibrator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Mapping narrative tension curves and identifying optimal cliffhanger moments to maximize coin-unlock retention.</div>',
    unsafe_allow_html=True
)

# ----------------- Processing Pipeline -----------------
beats = parse_script_into_beats(active_script)
scored_beats = calculate_tension_curve(beats)
cliffhangers = detect_optimal_cliffhangers(scored_beats)

# Macro Metrics
avg_tension = sum(b["smoothed_tension"] for b in scored_beats) / max(1, len(scored_beats))
peak_tension = max((b["smoothed_tension"] for b in scored_beats), default=0)
top_hook_index = cliffhangers[0]["hook_index"] if cliffhangers else 7.5

# ----------------- KPI Cards Row -----------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val">{top_hook_index} / 10</div>
        <div class="metric-label">Max Hook Index (Heuristic)</div>
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
        <div class="metric-label">Optimal Binge Hooks</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    grade = "Tier 1: High Binge Impact" if top_hook_index >= 8.5 else ("Tier 2: Moderate Impact" if top_hook_index >= 7.0 else "Tier 3: Low Impact")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val" style="color:#fbbf24; font-size:16px; margin-top:2px;">{grade.split(':')[0]}</div>
        <div class="metric-label">{grade.split(':')[1]}</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- Main Visualization: Interactive Tension Wave -----------------
st.markdown("### 📈 Narrative Tension Wave & Scene Pacing")
st.caption("Tracking beat-by-beat dialogue velocity, stakes escalation, and information gaps across scenes.")

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

# Highlight Cliffhanger Cut Points with vertical reference lines
for idx, cut in enumerate(cliffhangers):
    fig.add_vline(
        x=cut["beat_index"],
        line_width=2,
        line_dash="dash",
        line_color="#38bdf8" if idx == 0 else "#94a3b8",
        annotation_text=f"Cut #{idx+1} (Index: {cut['hook_index']})",
        annotation_position="top left",
        annotation_font=dict(size=10, color="#ffffff")
    )

fig.update_layout(
    height=320,
    margin=dict(l=10, r=10, t=25, b=10),
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    xaxis=dict(
        title="Narrative Beat Progression (Chronological)",
        gridcolor="#1e293b",
        color="#94a3b8"
    ),
    yaxis=dict(
        title="Tension Score (0 - 100)",
        gridcolor="#1e293b",
        color="#94a3b8",
        range=[15, 105]
    ),
    hovermode="x unified",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ----------------- Bottom Section: Cut Recommendations & A/B Hook Doctor -----------------
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### ✂️ Recommended Episode Cut Points")
    st.caption("Heuristically graded moments to roll credits on, leaving the viewer at peak cognitive tension.")
    
    for i, cut in enumerate(cliffhangers):
        badge_label = "🏆 Recommended Cut" if i == 0 else f"Alternative Option #{i+1}"
        st.markdown(f"""
        <div class="cut-card">
            <div class="cut-title">
                <span>{badge_label} • {cut['scene']}</span>
                <span class="badge-index">⚡ Hook Index: {cut['hook_index']} / 10 ({cut['tier']})</span>
            </div>
            <div class="cut-quote">
                <b>{cut['character']}:</b> "{cut['line']}"
            </div>
            <div style="font-size:11px; color:#cbd5e1; margin-bottom:6px;">
                <b>Hypothesis:</b> {cut['hypothesis']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable Transparent Rubric Breakdown
        with st.expander(f"🔍 View Scoring Rubric Breakdown for Cut #{i+1}"):
            r_cols = st.columns(3)
            rb = cut["rubric_breakdown"]
            with r_cols[0]:
                st.metric("Tension Base", f"{rb['Narrative Tension Base']} / 5.0")
            with r_cols[1]:
                st.metric("Information Gap", f"+{rb['Information Gap Withheld']}")
            with r_cols[2]:
                st.metric("Stakes Escalation", f"+{rb['Stakes Escalation']}")
            
            st.caption(f"**Dialogue Delivery:** {cut['pacing']} • Status Inversion Dynamic: +{rb['Status Inversion Dynamic']}")

with col_right:
    st.markdown("### 🧪 A/B Test Hook Doctor")
    st.caption("Generate distinct psychological variations for episode cliffhangers ready for production A/B testing.")
    
    # Pick a scene beat that could be improved
    sample_weak = scored_beats[min(4, len(scored_beats)-1)]
    ab_rewrites = generate_ab_test_rewrites(sample_weak)
    
    st.markdown("**Original Scene Ending:**")
    st.code(sample_weak["text"], language="markdown")
    
    # Variant A
    va = ab_rewrites["variant_a"]
    st.markdown(f"**Option 1: {va['title']}**")
    st.code(va["line"], language="markdown")
    st.caption(f"🎯 *Psychological Mechanism:* {va['psychological_lever']}")
    
    # Variant B
    vb = ab_rewrites["variant_b"]
    st.markdown(f"**Option 2: {vb['title']}**")
    st.code(vb["line"], language="markdown")
    st.caption(f"🎯 *Psychological Mechanism:* {vb['psychological_lever']}")
    
    st.markdown("---")
    st.markdown("### 📊 Pandas-to-SQL Analytics Pipeline")
    st.caption("Export structured narrative telemetry directly into your Snowflake / BigQuery / Power BI drop-off correlation pipeline.")
    
    analytics_df = export_normalized_analytics_dataset(scored_beats, cliffhangers)
    csv_bytes = analytics_df.to_csv(index=False).encode("utf-8")
    
    st.download_button(
        label="📥 Download Normalized Analytics CSV (for SQL/BI)",
        data=csv_bytes,
        file_name="hookgenius_script_telemetry.csv",
        mime="text/csv",
        use_container_width=True
    )
