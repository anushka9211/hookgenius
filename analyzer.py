"""
HookGenius Narrative Tension & Cliffhanger Analytics Engine v2.0
Designed for Kuku TV & Kuku FM Content Operations & Growth Engineering
"""

import re
import time
from typing import List, Dict, Any, Tuple
import pandas as pd

# High-yield dramatic conflict & revelation vocabulary for Indian OTT & Micro-Dramas
CONFLICT_KEYWORDS = {
    "high_conflict": [
        "kill", "murder", "dead", "death", "die", "poison", "cyanide", "blood", "gun", 
        "destroy", "ruin", "revenge", "betray", "betrayal", "suicide", "crash", "explosion",
        "arrest", "police", "jail", "raid", "freeze", "bankrupt", "cheat", "affair", "mistress",
        "slap", "strangle", "threat", "destroy", "choke", "drown"
    ],
    "power_reversal": [
        "own", "bought", "empire", "heir", "fortune", "crore", "5000", "500", "assets",
        "foreclosure", "guarantor", "trust fund", "power of attorney", "deed", "shares",
        "blackstone", "singhania", "oberoi", "raichand", "beggar", "street", "billionaire"
    ],
    "revelation_mystery": [
        "secret", "truth", "confession", "tape", "recording", "cctv", "camera", "real father",
        "real mother", "dna", "test", "fake", "faked", "impostor", "investigator", "evidence",
        "proof", "document", "contract", "pregnant", "wife", "hospital", "alive"
    ]
}

HOOK_TRIGGERS = [
    {
        "type": "Lethal Countdown & Physical Threat",
        "keywords": ["minute", "seconds", "cyanide", "poison", "heart", "die", "blood", "stop your heart"],
        "hypothesis": "Triggers immediate biological urgency. Listeners cannot disengage until survival is resolved."
    },
    {
        "type": "Status Inversion & Hierarchy Reversal",
        "keywords": ["real father", "heir", "dna", "son", "mother", "sharda", "raichand", "impostor", "beggar"],
        "hypothesis": "Dismantles the power dynamic, creating a cognitive cliffhanger around the oppressor's reaction."
    },
    {
        "type": "Sudden Financial Liquidation",
        "keywords": ["own", "bought", "freeze", "shares", "assets", "foreclosure", "crore", "bankrupt", "accounts are frozen"],
        "hypothesis": "Instant stakes escalation. The antagonist's primary defense mechanism is dissolved in one sentence."
    },
    {
        "type": "Unresolved Evidence Drop",
        "keywords": ["tape", "recording", "camera", "cctv", "document", "proof", "listen", "play", "investigator"],
        "hypothesis": "Promises an imminent explosive revelation, creating a high information gap."
    }
]


def parse_script_into_beats(script_text: str) -> List[Dict[str, Any]]:
    """
    Parses a screenplay / script into narrative beats (scenes, dialogues, stage directions).
    """
    lines = script_text.strip().split("\n")
    beats = []
    current_scene = "SCENE 1"
    beat_index = 1

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Detect Scene Headers
        if stripped.upper().startswith("SCENE ") or stripped.upper().startswith("INT.") or stripped.upper().startswith("EXT."):
            current_scene = stripped
            beats.append({
                "index": beat_index,
                "type": "SCENE_HEADER",
                "character": "DIRECTION",
                "text": stripped,
                "scene": current_scene
            })
            beat_index += 1
            continue

        # Detect Character Names (e.g. "VIKRAM" or "VIKRAM (Smirking)")
        match_char = re.match(r"^([A-Z\s]{2,20})(?:\s*\((.*?)\))?$", stripped)
        if match_char and not stripped.startswith("(") and len(stripped) < 30:
            char_name = match_char.group(1).strip()
            parenthetical = match_char.group(2) or ""
            beats.append({
                "index": beat_index,
                "type": "CHARACTER",
                "character": char_name,
                "parenthetical": parenthetical,
                "text": stripped,
                "scene": current_scene
            })
            beat_index += 1
            continue

        # Regular dialogue or action
        last_beat = beats[-1] if beats else None
        char = last_beat["character"] if (last_beat and last_beat["type"] == "CHARACTER") else "ACTION"
        
        beats.append({
            "index": beat_index,
            "type": "DIALOGUE" if char != "ACTION" else "ACTION",
            "character": char,
            "text": stripped,
            "scene": current_scene
        })
        beat_index += 1

    return beats


def calculate_tension_curve(beats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes beat-by-beat tension using a rolling narrative context window,
    dialogue velocity, and semantic stakes density.
    """
    scored_beats = []
    running_tension = 35.0  # Baseline tension
    accumulated_scene_stakes = 0.0
    current_scene_tracker = ""

    for b in beats:
        text_lower = b["text"].lower()
        score = running_tension

        # Context Window: Reset or carry scene-level narrative momentum
        if b["scene"] != current_scene_tracker:
            current_scene_tracker = b["scene"]
            accumulated_scene_stakes = min(20.0, accumulated_scene_stakes * 0.5)

        # 1. Pacing & Dialogue Staccato (Rapid turn-taking increases heart rate)
        words = b["text"].split()
        word_count = len(words)
        pacing_velocity = "Moderate"

        if 2 <= word_count <= 14 and b["type"] == "DIALOGUE":
            score += 9.0
            pacing_velocity = "High (Staccato)"
        elif word_count > 35:
            score -= 6.0
            pacing_velocity = "Low (Exposition)"

        # 2. Punctuation Shock (High arousal markers)
        arousal_markers = []
        if "?" in b["text"] and "!" in b["text"]:
            score += 12.0
            arousal_markers.append("Interrogative Shock (?! )")
        elif "!" in b["text"]:
            score += 7.0
            arousal_markers.append("Exclamation")
        elif "..." in b["text"]:
            score += 5.0
            arousal_markers.append("Trailing Suspense (...)")

        # 3. Conflict Rubric Flags
        stakes_escalated = False
        status_inversion = False
        info_withheld = False

        for kw in CONFLICT_KEYWORDS["high_conflict"]:
            if kw in text_lower:
                score += 14.0
                stakes_escalated = True
                accumulated_scene_stakes += 2.5
                break

        for kw in CONFLICT_KEYWORDS["power_reversal"]:
            if kw in text_lower:
                score += 13.0
                status_inversion = True
                accumulated_scene_stakes += 2.0
                break

        for kw in CONFLICT_KEYWORDS["revelation_mystery"]:
            if kw in text_lower:
                score += 14.0
                info_withheld = True
                accumulated_scene_stakes += 3.0
                break

        # Context multiplier: Past stakes elevate the current baseline
        score += accumulated_scene_stakes

        # Clamp between 15 and 99
        score = max(15.0, min(99.0, score))
        
        # Momentum smoothing: 65% carried forward, 35% current beat
        running_tension = 0.65 * running_tension + 0.35 * score

        scored_beats.append({
            **b,
            "word_count": word_count,
            "raw_tension": round(score, 1),
            "smoothed_tension": round(running_tension, 1),
            "pacing_velocity": pacing_velocity,
            "arousal_markers": arousal_markers,
            "rubric_flags": {
                "stakes_escalated": stakes_escalated,
                "status_inversion": status_inversion,
                "information_withheld": info_withheld
            }
        })

    return scored_beats


def detect_optimal_cliffhangers(scored_beats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Identifies top episode cut points and outputs an interpretable Hook Index (0-10)
    with a fully transparent grading rubric breakdown.
    """
    candidates = []

    for i, b in enumerate(scored_beats):
        if b["type"] == "SCENE_HEADER" or len(b["text"]) < 10:
            continue

        text_lower = b["text"].lower()
        raw_score = b["smoothed_tension"]

        # Check for matched trigger hypothesis
        matched_trigger = None
        for trig in HOOK_TRIGGERS:
            for kw in trig["keywords"]:
                if kw in text_lower:
                    matched_trigger = trig
                    break
            if matched_trigger:
                break

        # Transparent Component Weights for Hook Index
        rubric = b.get("rubric_flags", {})
        info_gap = rubric.get("information_withheld", False) or ("?" in b["text"])
        stakes = rubric.get("stakes_escalated", False)
        inversion = rubric.get("status_inversion", False)
        is_dialogue = b["character"] not in ["ACTION", "DIRECTION"]

        # Calculate Rubric Breakdown (Max 10.0)
        rubric_breakdown = {
            "Narrative Tension Base": round(raw_score / 20.0, 2),  # up to 5.0
            "Information Gap Withheld": 2.2 if info_gap else 0.4,
            "Stakes Escalation": 1.8 if stakes else 0.5,
            "Status Inversion Dynamic": 1.5 if inversion else 0.2,
            "Dialogue Delivery Penalty": 0.0 if is_dialogue else -1.5
        }

        hook_index = sum(rubric_breakdown.values())
        hook_index = round(min(9.9, max(2.0, hook_index)), 1)

        # Categorical Tier
        if hook_index >= 8.5:
            tier = "Tier 1: High Binge Impact"
        elif hook_index >= 7.0:
            tier = "Tier 2: Moderate Binge Impact"
        else:
            tier = "Tier 3: Low Binge Impact"

        if hook_index >= 7.0:
            candidates.append({
                "beat_index": b["index"],
                "scene": b["scene"],
                "character": b["character"],
                "line": b["text"],
                "tension": round(raw_score, 1),
                "hook_index": hook_index,
                "tier": tier,
                "trigger_type": matched_trigger["type"] if matched_trigger else "Confrontational Impasse",
                "hypothesis": matched_trigger["hypothesis"] if matched_trigger else "Leaves a major character confrontation unresolved.",
                "rubric_breakdown": rubric_breakdown,
                "pacing": b["pacing_velocity"]
            })

    # Sort descending by Hook Index
    candidates.sort(key=lambda x: x["hook_index"], reverse=True)

    # Pick distinct cuts (separated by at least 2 beats)
    unique_cuts = []
    seen_indices = set()
    for c in candidates:
        idx = c["beat_index"]
        if not any(abs(idx - s) <= 2 for s in seen_indices):
            unique_cuts.append(c)
            seen_indices.add(idx)
        if len(unique_cuts) >= 3:
            break

    return unique_cuts


def generate_ab_test_rewrites(weak_beat: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hook Doctor: Generates two distinct, testable psychological variations for A/B testing.
    Variant A: Loss Aversion / Lethal Countdown
    Variant B: Identity Reveal / Cognitive Gap
    """
    original = weak_beat.get("text", "")
    char = weak_beat.get("character", "CHARACTER")

    variant_a = {
        "title": "Variant A: Loss Aversion & Urgent Countdown",
        "line": f"{char}\n(Whispers, stepping closer)\n\"You have exactly three minutes before the auditors freeze this building. And you won't like what they find in your safe.\"",
        "psychological_lever": "Immediate survival clock / irreversible asset loss."
    }

    variant_b = {
        "title": "Variant B: Status Inversion & Identity Reveal",
        "line": f"{char}\n(Smiles coldly, sliding a black folder onto the marble)\n\"Before you call security, Vikram... check page two. The DNA test proves who really inherits this house.\"",
        "psychological_lever": "Destroys character status hierarchy; unresolved identity question."
    }

    return {
        "original": original,
        "variant_a": variant_a,
        "variant_b": variant_b
    }


def compute_telemetry(script_text: str, start_time: float) -> Dict[str, Any]:
    """
    Computes production unit economics & latency telemetry.
    """
    word_count = len(script_text.split())
    # Estimated tokens: ~1.33 tokens per English/Hinglish word
    est_tokens = int(word_count * 1.33)
    # Gemini 3.8 Flash Pricing benchmark: ~$0.75 per 1M input tokens (~₹62 per 1M tokens)
    est_cost_inr = round((est_tokens / 1_000_000) * 62.0, 4)
    elapsed_sec = round(time.time() - start_time, 2)

    return {
        "word_count": word_count,
        "est_tokens": est_tokens,
        "cost_inr": f"₹{est_cost_inr:.3f}",
        "latency_sec": f"{elapsed_sec}s"
    }


def export_normalized_analytics_dataset(scored_beats: List[Dict[str, Any]], cliffhangers: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Exports a clean, normalized DataFrame ready for correlation analysis in SQL/Snowflake.
    """
    cut_indices = {c["beat_index"]: c["hook_index"] for c in cliffhangers}
    records = []

    for b in scored_beats:
        is_cut = b["index"] in cut_indices
        records.append({
            "beat_id": b["index"],
            "scene_id": b["scene"],
            "speaker": b["character"],
            "beat_type": b["type"],
            "word_count": b.get("word_count", 0),
            "smoothed_tension": b["smoothed_tension"],
            "is_recommended_cut": is_cut,
            "hook_index": cut_indices.get(b["index"], None),
            "pacing_velocity": b.get("pacing_velocity", "Moderate"),
            "stakes_flag": b.get("rubric_flags", {}).get("stakes_escalated", False),
            "info_gap_flag": b.get("rubric_flags", {}).get("information_withheld", False)
        })

    return pd.DataFrame(records)
