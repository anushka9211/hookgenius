from sample_scripts import SAMPLE_SCRIPTS
from analyzer import parse_script_into_beats, calculate_tension_curve, detect_optimal_cliffhangers

for title, script in SAMPLE_SCRIPTS.items():
    beats = parse_script_into_beats(script)
    scored = calculate_tension_curve(beats)
    cuts = detect_optimal_cliffhangers(scored)
    print(f"\n=== {title} ===")
    for i, c in enumerate(cuts, 1):
        print(f"  Cut #{i}: [{c['character']}] \"{c['line'][:60]}...\" (Hook Index: {c['hook_index']})")
