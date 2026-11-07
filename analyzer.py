"""
HookGenius Narrative Tension & Cliffhanger Analytics Engine v2.5
Designed for Kuku TV & Kuku FM Content Operations & Growth Engineering
Features:
- Regex Word-Boundary Conflict Matching (Zero substring false positives)
- Absolute Anchored Scoring Rubric (Scores 1-3: Mundane, 4-6: Friction, 7-8: High Stakes, 9-10: Peak Inversion)
- Turn-Taking Retort Detection with Stakes Gating
- Native Negative Control / Flat Scene Support
"""

import re
import time
from typing import List, Dict, Any, Tuple
import pandas as pd

# High-yield dramatic conflict & revelation vocabulary for Indian OTT & Micro-Dramas
RAW_CONFLICT_KEYWORDS = {
    "high_conflict": [
        "kill", "murder", "dead", "death", "die", "poison", "cyanide", "blood", "gun", 
        "destroy", "ruin", "revenge", "betray", "betrayal", "suicide", "crash", "explosion",
        "arrest", "police", "jail", "raid", "freeze", "bankrupt", "cheat", "affair", "mistress",
        "slap", "strangle", "threat", "destroy", "choke", "drown", "scraps", "divorce", "forfeited"
    ],
    "power_reversal": [
        "own", "bought", "empire", "heir", "fortune", "crore", "5000", "500", "assets",
        "foreclosure", "guarantor", "trust fund", "power of attorney", "deed", "shares",
        "blackstone", "singhania", "oberoi", "raichand", "beggar", "street", "billionaire",
        "get out", "out of my house", "my house", "my company", "primary shareholder",
        "sole heir", "founder", "founded", "ceo", "audit", "kneel", "fired", "slave"
    ],
    "revelation_mystery": [
        "secret", "truth", "confession", "tape", "recording", "cctv", "camera", "real father",
        "real mother", "dna", "test", "fake", "faked", "impostor", "investigator", "evidence",
        "proof", "confidential document", "contract", "pregnant", "hospital", "alive"
    ]
}

# Compile with strict regex word boundaries to prevent substring bleed (e.g. "down" matching "own")
COMPILED_CONFLICT_KEYWORDS = {
    cat: [re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE) for kw in kws]
    for cat, kws in RAW_CONFLICT_KEYWORDS.items()
}

HOOK_TRIGGERS = [
    {
        "type": "Status Inversion & Hierarchy Reversal",
        "keywords": ["real father", "heir", "dna", "son", "mother", "sharda", "raichand", "impostor", "beggar", "primary shareholder", "out of my house", "get out"],
        "hypothesis": "Dismantles the power dynamic, creating a cognitive cliffhanger around the oppressor's reaction."
    },
    {
        "type": "Lethal Countdown & Physical Threat",
        "keywords": ["minute", "seconds", "cyanide", "poison", "heart", "die", "blood", "stop your heart"],
        "hypothesis": "Triggers immediate biological urgency. Listeners cannot disengage until survival is resolved."
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
    Robustly tracks active speaker across parentheticals and line breaks.
    """
    lines = script_text.strip().split("\n")
    beats = []
    current_scene = "SCENE 1"
    current_speaker = None
    beat_index = 1

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Detect Scene Headers
        if stripped.upper().startswith("SCENE ") or stripped.upper().startswith("INT.") or stripped.upper().startswith("EXT."):
            current_scene = stripped
            current_speaker = None
            beats.append({
                "index": beat_index,
                "type": "SCENE_HEADER",
                "character": "DIRECTION",
                "text": stripped,
                "scene": current_scene
            })
            beat_index += 1
            continue

        # Skip Scene End tags
        if stripped.upper() in ["[SCENE END]", "[END]", "CUT TO BLACK", "FADE OUT"]:
            current_speaker = None
            continue

        # Detect Standalone Parentheticals e.g. "(Coldly)" or "(Voice steady)"
        if stripped.startswith("(") and stripped.endswith(")"):
            beats.append({
                "index": beat_index,
                "type": "PARENTHETICAL",
                "character": current_speaker or "DIRECTION",
                "text": stripped,
                "scene": current_scene
            })
            beat_index += 1
            continue

        # Detect Character Names (e.g. "VIKRAM" or "VIKRAM (Smirking)")
        match_char = re.match(r"^([A-Z\s]{2,25})(?:\s*\((.*?)\))?$", stripped)
        is_known_non_char = any(k in stripped.upper() for k in ["SCENE", "INT.", "EXT.", "DAY", "NIGHT", "STUDY"])
        if match_char and not stripped.startswith("(") and len(stripped) < 30 and not is_known_non_char:
            char_name = match_char.group(1).strip()
            parenthetical = match_char.group(2) or ""
            current_speaker = char_name
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

        # If current_speaker is active, this line is DIALOGUE
        if current_speaker:
            beats.append({
                "index": beat_index,
                "type": "DIALOGUE",
                "character": current_speaker,
                "text": stripped,
                "scene": current_scene
            })
            beat_index += 1
            current_speaker = None  # Reset speaker until next character cue
            continue

        # Otherwise it's ACTION / Stage direction
        beats.append({
            "index": beat_index,
            "type": "ACTION",
            "character": "ACTION",
            "text": stripped,
            "scene": current_scene
        })
        beat_index += 1

    return beats


def calculate_tension_curve(beats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes beat-by-beat tension using strict semantic stakes gating.
    Mundane small talk remains flatlined near baseline (10-20), while dramatic
    conflict accelerates towards climax (70-99).
    """
    scored_beats = []
    running_tension = 15.0  # True resting baseline for human conversations
    accumulated_scene_stakes = 0.0
    current_scene_tracker = ""

    scene_beat_counts: Dict[str, int] = {}
    for b in beats:
        scene_beat_counts[b["scene"]] = scene_beat_counts.get(b["scene"], 0) + 1

    scene_current_indices: Dict[str, int] = {}

    for i, b in enumerate(beats):
        scene_name = b["scene"]
        scene_current_indices[scene_name] = scene_current_indices.get(scene_name, 0) + 1
        scene_progress = scene_current_indices[scene_name] / max(1, scene_beat_counts.get(scene_name, 1))

        if scene_name != current_scene_tracker:
            current_scene_tracker = scene_name
            accumulated_scene_stakes = 0.0
            running_tension = 15.0

        words = b["text"].split()
        word_count = len(words)
        pacing_velocity = "Moderate"

        # Regex word-boundary keyword checks
        stakes_escalated = any(r.search(b["text"]) for r in COMPILED_CONFLICT_KEYWORDS["high_conflict"])
        status_inversion = any(r.search(b["text"]) for r in COMPILED_CONFLICT_KEYWORDS["power_reversal"])
        info_withheld = any(r.search(b["text"]) for r in COMPILED_CONFLICT_KEYWORDS["revelation_mystery"])

        has_conflict = stakes_escalated or status_inversion or info_withheld

        if stakes_escalated:
            accumulated_scene_stakes += 5.0
        if status_inversion:
            accumulated_scene_stakes += 6.0
        if info_withheld:
            accumulated_scene_stakes += 5.0

        # Rapid decay if no ongoing conflict exists
        if not has_conflict:
            accumulated_scene_stakes = max(0.0, accumulated_scene_stakes * 0.70)

        arousal_markers = []
        is_punchline_retort = False

        # --- BRANCH A: MUNDANE / SMALL TALK (Negative Control Zone) ---
        if not has_conflict and accumulated_scene_stakes < 2.0:
            target_score = 12.0
            if "?" in b["text"]:
                target_score += 4.0  # Minor transactional curiosity ripple
                arousal_markers.append("Routine Query")
            if 1 <= word_count <= 8 and b["type"] == "DIALOGUE":
                pacing_velocity = "Casual Banter"

        # --- BRANCH B: ACTIVE DRAMATIC CONFLICT (High Stakes Zone) ---
        else:
            target_score = 25.0 + accumulated_scene_stakes
            if 1 <= word_count <= 12 and b["type"] == "DIALOGUE":
                target_score += 10.0
                pacing_velocity = "High (Staccato)"
            elif word_count > 35:
                target_score -= 6.0
                pacing_velocity = "Low (Exposition)"

            if "?" in b["text"] and "!" in b["text"]:
                target_score += 14.0
                arousal_markers.append("Interrogative Shock (?! )")
            elif "!" in b["text"]:
                target_score += 8.0
                arousal_markers.append("Exclamation")
            elif "..." in b["text"]:
                target_score += 5.0
                arousal_markers.append("Trailing Suspense (...)")

            if stakes_escalated:
                target_score += 16.0
            if status_inversion:
                target_score += 18.0
            if info_withheld:
                target_score += 16.0

            # Turn-Taking Retort Detection: ONLY active during dramatic conflict
            if i > 0 and b["type"] == "DIALOGUE" and word_count <= 14 and accumulated_scene_stakes >= 4.0:
                prev_dialogue_beat = None
                for prev_k in range(i - 1, -1, -1):
                    if beats[prev_k]["type"] == "DIALOGUE":
                        prev_dialogue_beat = beats[prev_k]
                        break
                    elif beats[prev_k]["type"] in ["SCENE_HEADER", "ACTION"]:
                        break
                
                if prev_dialogue_beat and "?" in prev_dialogue_beat["text"] and prev_dialogue_beat["character"] != b["character"]:
                    target_score += 22.0
                    is_punchline_retort = True
                    status_inversion = True
                    arousal_markers.append("Climactic Punchline Retort")

        # Clamp between 10 and 99
        target_score = max(10.0, min(99.0, target_score))
        
        # Momentum smoothing: In mundane mode, snaps down quickly to baseline
        alpha = 0.55 if accumulated_scene_stakes < 2.0 else 0.40
        running_tension = (1.0 - alpha) * running_tension + alpha * target_score

        scored_beats.append({
            **b,
            "word_count": word_count,
            "scene_progress": round(scene_progress, 2),
            "raw_tension": round(target_score, 1),
            "smoothed_tension": round(running_tension, 1),
            "pacing_velocity": pacing_velocity,
            "arousal_markers": arousal_markers,
            "is_punchline_retort": is_punchline_retort,
            "accumulated_stakes": round(accumulated_scene_stakes, 1),
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
    using strict Absolute Anchors:
    - Scores 1-3: Mundane daily activity, small talk, office chores, zero stakes.
    - Scores 4-6: Mild friction, emotional arguments, no irreversible damage.
    - Scores 7-8: Severe stakes raised, large financial loss, blackmail, physical danger.
    - Scores 9-10: Peak biological urgency, complete status inversion, terminal mic-drop.
    """
    candidates = []

    for i, b in enumerate(scored_beats):
        if b["type"] in ["SCENE_HEADER", "PARENTHETICAL", "CHARACTER"] or len(b["text"]) < 4:
            continue

        raw_score = b["smoothed_tension"]
        rubric = b.get("rubric_flags", {})
        info_gap = rubric.get("information_withheld", False)
        stakes = rubric.get("stakes_escalated", False)
        inversion = rubric.get("status_inversion", False)
        is_dialogue = b["type"] == "DIALOGUE"
        is_retort = b.get("is_punchline_retort", False)
        scene_prog = b.get("scene_progress", 0.5)
        stakes_level = b.get("accumulated_stakes", 0.0)

        # --- ABSOLUTE ANCHORED RUBRIC FORMULA ---
        if stakes_level < 2.0 and not (stakes or inversion or info_gap):
            # ANCHOR 1-3: MUNDANE / NEGATIVE CONTROL
            hook_index = round(min(2.5, 0.5 + (raw_score / 20.0)), 1)
            tier = "Tier 3: Low Binge Impact (Mundane Scene)"
            is_climax_apex = False
            rubric_breakdown = {
                "Narrative Tension Base": round(raw_score / 25.0, 2),
                "Information Gap Withheld": 0.3 if "?" in b["text"] else 0.1,
                "Stakes Escalation": 0.0,
                "Status Inversion Dynamic": 0.0,
                "Climax Mic-Drop Positioning": 0.0,
                "Mundane Office/Chore Baseline Cap": "Active (Scores 1-3)"
            }
        elif stakes_level < 8.0 and not is_retort:
            # ANCHOR 4-6: MILD FRICTION
            hook_index = round(min(6.5, 3.5 + (raw_score / 25.0)), 1)
            tier = "Tier 2: Moderate Binge Impact"
            is_climax_apex = False
            rubric_breakdown = {
                "Narrative Tension Base": round(raw_score / 22.0, 2),
                "Information Gap Withheld": 1.0 if info_gap else 0.4,
                "Stakes Escalation": 1.2 if stakes else 0.3,
                "Status Inversion Dynamic": 0.8 if inversion else 0.2,
                "Climax Mic-Drop Positioning": 0.0,
                "Dialogue Delivery": 0.0 if is_dialogue else -1.0
            }
        else:
            # ANCHOR 7-10: HIGH STAKES & CLIMACTIC STATUS INVERSION
            climax_bonus = 2.8 if is_retort else (1.6 if scene_prog >= 0.75 else 0.0)
            is_climax_apex = is_retort or (scene_prog >= 0.85)
            tension_base = round(raw_score / 22.0, 2)

            rubric_breakdown = {
                "Narrative Tension Base": min(4.5, tension_base),
                "Information Gap Withheld": 1.8 if info_gap else 0.4,
                "Stakes Escalation": 1.6 if stakes else 0.4,
                "Status Inversion Dynamic": 2.2 if inversion else 0.2,
                "Climax Mic-Drop Positioning": climax_bonus,
                "Dialogue Delivery Penalty": 0.0 if is_dialogue else -1.8
            }
            hook_index = sum(v for v in rubric_breakdown.values() if isinstance(v, (int, float)))
            hook_index = round(min(9.9, max(7.0, hook_index)), 1)
            tier = "Tier 1: High Binge Impact" if hook_index >= 8.5 else "Tier 2: Moderate Binge Impact"

        # Check matched trigger
        matched_trigger = None
        for trig in HOOK_TRIGGERS:
            for kw in trig["keywords"]:
                if re.search(r"\b" + re.escape(kw) + r"\b", b["text"], re.IGNORECASE):
                    matched_trigger = trig
                    break
            if matched_trigger:
                break

        # Only register candidate cuts if hook_index meets minimal threshold (>= 7.0 for recommendation)
        if hook_index >= 7.0:
            candidates.append({
                "beat_index": b["index"],
                "scene": b["scene"],
                "character": b["character"],
                "line": b["text"],
                "tension": round(raw_score, 1),
                "hook_index": hook_index,
                "is_climax_apex": is_climax_apex,
                "scene_progress": scene_prog,
                "tier": tier,
                "trigger_type": matched_trigger["type"] if matched_trigger else "Status Inversion Mic-Drop",
                "hypothesis": matched_trigger["hypothesis"] if matched_trigger else "Leaves character power hierarchy completely flipped at peak emotional shock.",
                "rubric_breakdown": rubric_breakdown,
                "pacing": b["pacing_velocity"]
            })

    # Sort descending prioritizing Hook Index, then Climax Apex, Scene Progress, Beat Index
    candidates.sort(key=lambda x: (x["hook_index"], x["is_climax_apex"], x["scene_progress"], x["beat_index"]), reverse=True)

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
