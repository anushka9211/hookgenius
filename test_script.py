from analyzer import parse_script_into_beats, calculate_tension_curve, detect_optimal_cliffhangers

script = '''SCENE 1: INT. SINGHANIA MANSION - STUDY - DAY

TANYA (28, dressed in designer wear) throws a thick legal file onto the mahogany desk. ARJUN (30, dressed in simple cotton clothes) looks at it calmly. VIKRAM (32, arrogant) smirks from the corner of the room.

TANYA
Sign it, Arjun. You have lived off my family's scraps for three long years. Our marriage is over. The 500-crore enterprise belongs to me.

ARJUN
(Voice steady)
Are you entirely sure about this, Tanya? Once my signature is on that paper, there is no going back.

VIKRAM
(Laughs)
Stop stalling, you beggar! We have a press board meeting in twenty minutes to announce Tanya as the new CEO. Sign the divorce deed and take your suitcase out the back door.

Arjun picks up the gold-plated pen. He doesn't read the document. He just signs it in one fluid motion and slides it across the desk.

Tanya snatches it eagerly.

TANYA
Finally. Mr. Sharma!

MR. SHARMA (50s, the family lawyer) steps forward. He takes the file to verify the signature. As he scans the document, his phone buzzes. He looks at an urgent email. The color completely drains from his face.

MR. SHARMA
(Trembling)
Madam... there is a severe problem.

TANYA
What problem? He signed it. We own 100% of Singhania Industries now.

MR. SHARMA
No, madam. The original guarantor deed from 1999 just cleared the Supreme Court. The true heir to the Singhania empire... it isn't your late father.

TANYA
What nonsense are you talking about?! I am the only bloodline!

Suddenly, the heavy oak doors burst open. Four armed security guards in black suits march in, completely ignoring Tanya and Vikram. They stand at attention behind Arjun.

ARJUN
(Slowly stands up, buttoning his jacket)
Mr. Sharma is telling the truth, Tanya. My grandfather founded this company. I only married you to audit the accounts from the inside.

Vikram takes a step back, terrified. Tanya drops the file.

ARJUN
And by signing that mutual divorce deed... you didn't legally separate from me. You just forfeited your 20% minority stake back to the primary shareholder.

TANYA
(Breathless, shaking)
Primary shareholder? Who... who is the primary shareholder?

ARJUN
(Coldly)
Me. Now get out of my house.

[SCENE END]'''

beats = parse_script_into_beats(script)
scored = calculate_tension_curve(beats)
cuts = detect_optimal_cliffhangers(scored)

print("\n--- FINAL RECOMMENDED CUTS ---")
for i, c in enumerate(cuts, 1):
    print(f"Top Cut #{i}: [{c['character']}] \"{c['line']}\" | Hook Index: {c['hook_index']} | Tier: {c['tier']}")
