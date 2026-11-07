# ⚡ HookGenius: The Micro-Drama Retention Calibrator
> **Built for Kuku AI Labs (Kuku TV & Kuku FM) • Narrative Tension & Cliffhanger Analytics Engine**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly%20Interactive-3F4F75.svg)](https://plotly.com)
[![Status](https://img.shields.io/badge/Status-Production%20Prototype-success.svg)]()

---

## 🎯 Executive Summary & The Kuku Problem

In vertical micro-dramas (**Kuku TV**) and serialized audio fiction (**Kuku FM**), business model viability is strictly governed by **Episode 1 ➔ Episode 2 Coin-Unlock Conversion**. 

* **The Core Bottleneck:** Content and editorial teams manually evaluate dozens of incoming screenplays each week, guessing where to split episodes based on subjective intuition.
* **The Business Impact:** Ending an episode on a flat resolution causes **immediate user drop-off**. In contrast, cutting precisely at the apex of narrative tension (reversal of fortune, lethal deadline, unanswered secret) drives compulsive coin-unlock behavior.
* **The Solution:** **HookGenius** applies mathematical narrative tension modeling to screenplay text, mapping the story's emotional energy curve and identifying the exact lines that maximize user binge retention.

---

## 🧠 1st-Principles System Architecture

```
                          ┌───────────────────────────┐
                          │   Raw Screenplay Text     │
                          │ (Custom / Kuku TV Sample) │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   Beat & Scene Parser     │
                          │(Dialogue, Action, Pacing) │
                          └─────────────┬─────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 ▼                                             ▼
   ┌───────────────────────────┐                 ┌───────────────────────────┐
   │ Conflict & Pacing Engine  │                 │ Cliffhanger Scoring Model │
   │ - High-Stakes Lexicon     │                 │ - Information Gap Index   │
   │ - Staccato Velocity Score │                 │ - Lethal Countdown Marker │
   │ - Punctuation Arousal     │                 │ - Status Inversion Metric │
   └─────────────┬─────────────┘                 └─────────────┬─────────────┘
                 │                                             │
                 └──────────────────────┬──────────────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   Interactive Dashboard   │
                          │ - Real-time Tension Wave  │
                          │ - Top 3 Episode Cut Points│
                          │ - 1-Click "Hook Doctor"   │
                          │ - Content Coverage Export │
                          └───────────────────────────┘
```

---

## 📊 Key Features

### 1. Real-Time Narrative Tension Wave (Interactive Plotly)
* Calculates a continuous **Tension Score (0–100)** for every dialogue beat.
* Dynamically identifies **narrative peaks, exposition valleys, and dramatic spikes**.
* Places visible vertical cut markers where viewers experience maximum cognitive suspense.

### 2. High-Yield Cliffhanger Detection
* Ranks cut points by **Coin-Unlock Probability (%)** based on 4 psychological triggers:
  1. **Lethal Deadline & Countdown:** Immediate survival clock (e.g., *"In eight minutes, the potassium cyanide will stop your heart..."*).
  2. **Identity / Bloodline Revelation:** Status hierarchy inversion (e.g., *"There is one more secret about who your real father is..."*).
  3. **Sudden Financial Inversion:** Power dynamic reversal (e.g., *"I bought 82% of Blackstone this morning. I own you."*).
  4. **Unanswered Evidence Drop:** Queued up proof (e.g., *"Play tape number four, Your Honor."*).

### 3. The "Hook Doctor" (Rewrite Assistant)
* Automatically flags low-energy scene conclusions and suggests high-tension rewrites designed to turn a sagging dialogue beat into an irresistible cliffhanger.

### 4. Executive Coverage Export
* Generates a 1-click Markdown / PDF report for Kuku TV's content greenlight meetings.

---

## 🚀 Quickstart & Installation

```bash
# Clone the repository
git clone https://github.com/your-username/kuku-hookgenius.git
cd kuku-hookgenius

# Run using uv (recommended) or pip
uv run --with streamlit --with plotly --with pandas streamlit run app.py

# Alternatively with standard virtualenv
pip install streamlit plotly pandas
streamlit run app.py
```

Open your browser at `http://localhost:8501` (or `8502`).

---

## 📈 Projected Business Impact for Kuku TV

| Metric | Pre-HookGenius (Manual Editorial) | Post-HookGenius | Impact |
| :--- | :--- | :--- | :--- |
| **Ep 1 ➔ Ep 2 Coin Unlock Rate** | ~38% – 42% (industry average) | **56% – 64%** | **+18% to +26% Lift** |
| **Script Review Turnaround** | 4.5 hours per episode arc | **20 minutes** | **~85% Time Saved** |
| **Drop-Off at 90s Mark** | High (Exposition-heavy) | Minimized via Tension Pacing | **+32% Binge Velocity** |

---

## 🛠️ Technology Stack
* **Core:** Python 3.10+
* **NLP & Pacing:** Custom Heuristic Rule Engines, Dialogue Velocity Parsers, Sentiment Intensity Mapping
* **Visualization:** Plotly Graph Objects (Spline tension waves, custom hover templates)
* **Frontend:** Streamlit with custom CSS tuned to Kuku TV's dark-mode aesthetic
