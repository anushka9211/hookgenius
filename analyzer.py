"""
HookGenius Narrative Tension & Cliffhanger Analytics Engine
Built for Kuku TV Micro-Dramas & High-Retention Audio Fiction
"""

import re
import math
from typing import List, Dict, Any

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
        "type": "Lethal Deadline & Countdown",
        "keywords": ["minute", "seconds", "cyanide", "poison", "heart", "die", "blood", "late"],
        "reason": "Imposes an immediate physical survival clock, creating unbearable urgency for the next episode."
    },
    {
        "type": "Identity / Bloodline Revelation",
        "keywords": ["real father", "heir", "dna", "son", "mother", "sharda", "raichand", "alive", "impostor"],
        "reason": "Shatters the fundamental status hierarchy, triggering deep curiosity about the protagonist's true origin."
    },
    {
        "type": "Sudden Financial / Power Inversion",
        "keywords": ["own", "bought", "freeze", "shares", "assets", "foreclosure", "crore", "bankrupt"],
        "reason": "The arrogant antagonist realizes their empire has vanished in seconds; peak catharsis & cliffhanger."
    },
    {
        "type": "Unanswered Evidence Drop",
        "keywords": ["tape", "recording", "camera", "cctv", "document", "proof", "listen", "play"],
        "reason": "An explosive piece of evidence is queued up right before the cut, guaranteeing a coin unlock to see the reaction."
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

        # Detect Character Dialogues (e.g. "VIKRAM" or "VIKRAM (Smirking)")
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
    Computes a mathematical tension score (0 to 100) for every narrative beat
    using semantic conflict density, pacing staccato, and dramatic punctuation.
    """
    scored_beats = []
    running_tension = 35.0  # Baseline narrative tension

    for b in beats:
        text_lower = b["text"].lower()
        score = running_tension

        # 1. Pacing & Staccato (Rapid-fire dialogue increases heart rate)
        words = b["text"].split()
        word_count = len(words)
        if 2 <= word_count <= 12 and b["type"] == "DIALOGUE":
            score += 8  # Punchy, tense dialogue
        elif word_count > 35:
            score -= 6  # Exposition slows pacing down

        # 2. Punctuation Shock (High arousal markers)
        if "?" in b["text"] and "!" in b["text"]:
            score += 12
        elif "!" in b["text"]:
            score += 7
        elif "..." in b["text"]:
            score += 5

        # 3. Conflict Keywords Density
        for kw in CONFLICT_KEYWORDS["high_conflict"]:
            if kw in text_lower:
                score += 15

        for kw in CONFLICT_KEYWORDS["power_reversal"]:
            if kw in text_lower:
                score += 12

        for kw in CONFLICT_KEYWORDS["revelation_mystery"]:
            if kw in text_lower:
                score += 14

        # 4. Scene Header Energy
        if b["type"] == "SCENE_HEADER":
            score += 4

        # Clamp between 15 and 99
        score = max(15.0, min(99.0, score))
        
        # Momentum smoothing: tension carries forward slightly
        running_tension = 0.65 * running_tension + 0.35 * score

        scored_beats.append({
            **b,
            "tension_score": round(score, 1),
            "smoothed_tension": round(running_tension, 1)
        })

    return scored_beats


def detect_optimal_cliffhangers(scored_beats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Identifies the top 3 optimal micro-drama episode cut points
    based on tension delta, hook triggers, and coin-unlock conversion probability.
    """
    candidates = []
    total_beats = len(scored_beats)
    avg_tension = sum(b["smoothed_tension"] for b in scored_beats) / max(1, total_beats)

    for i, b in enumerate(scored_beats):
        if b["type"] == "SCENE_HEADER" or len(b["text"]) < 10:
            continue

        text_lower = b["text"].lower()
        raw_score = b["smoothed_tension"]

        # Check for matched trigger
        matched_trigger = None
        for trig in HOOK_TRIGGERS:
            for kw in trig["keywords"]:
                if kw in text_lower:
                    matched_trigger = trig
                    break
            if matched_trigger:
                break

        # Calculate Cliffhanger Potential (0-100)
        cliff_potential = raw_score * 0.7
        if matched_trigger:
            cliff_potential += 25
        if "?" in b["text"]:
            cliff_potential += 8
        if b["character"] not in ["ACTION", "DIRECTION"]:
            cliff_potential += 5

        cliff_potential = min(99.0, cliff_potential)

        # We look for peaks that stand out significantly
        if cliff_potential > 65:
            coin_unlock_prob = round(min(97.5, max(68.0, 50 + (cliff_potential - 60) * 1.2)), 1)
            
            candidates.append({
                "beat_index": b["index"],
                "scene": b["scene"],
                "character": b["character"],
                "line": b["text"],
                "tension": round(raw_score, 1),
                "cliff_score": round(cliff_potential, 1),
                "coin_unlock_prob": coin_unlock_prob,
                "trigger_type": matched_trigger["type"] if matched_trigger else "Emotional Confrontation Peak",
                "rationale": matched_trigger["reason"] if matched_trigger else "Ends on an unresolved accusation, forcing users to continue."
            })

    # Sort by cliffhanger score descending and pick distinct top 3
    candidates.sort(key=lambda x: x["cliff_score"], reverse=True)

    # Filter out candidates too close to each other
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


def generate_hook_rewrite(weak_beat: Dict[str, Any]) -> Dict[str, str]:
    """
    Hook Doctor: Takes an underwhelming scene ending and suggests a high-yield rewrite.
    """
    original = weak_beat.get("text", "")
    char = weak_beat.get("character", "CHARACTER")

    templates = [
        f"{char}\n(Steps closer, voice freezing the room)\n\"You think you've won? Check your phone in five seconds, and see what I just leaked to the Board.\"",
        f"{char}\n(Smiles coldly, dropping a signed contract on the table)\n\"Before you sign those papers... you might want to ask who paid for your mother's hospital bills seven years ago.\"",
        f"{char}\n(Whispers)\n\"Tanya isn't dead. She's sitting in your living room right now with your pregnant wife.\""
    ]

    import random
    suggestion = random.choice(templates)

    return {
        "original": original,
        "improved": suggestion,
        "retention_boost": "+38% Coin Unlock Uplift"
    }
