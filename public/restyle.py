with open('team2.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacements = [
    ('#04060A', '#3a1020'),
    ('#0D1321', '#4A1828'),
    ('#A8892A', '#7DB547'),
    ('#C9A84C', '#7DB547'),
    ('#F5F3EE', '#f8f6f0'),
    ('#E8F2FA', '#f8f6f0'),
    ('#9BAFC4', 'rgba(74,24,40,0.65)'),
    ('#1a2235', '#7A2E42'),
    ('rgba(4, 6, 10, 0.92)', 'rgba(74, 24, 40, 0.96)'),
    ('rgba(168,137,42,', 'rgba(125,181,71,'),
    ('rgba(168, 137, 42,', 'rgba(125,181,71,'),
    ('var(--void)', 'var(--dark-burgundy)'),
    ('var(--navy)', 'var(--burgundy)'),
    ('var(--gold2)', 'var(--green)'),
    ('var(--gold)', 'var(--green)'),
    ('var(--cream)', 'var(--warm-white)'),
    ('var(--ink2)', 'var(--mid-burgundy)'),
    ('var(--navy-mid)', 'var(--mid-burgundy)'),
    ('var(--ink)', 'var(--warm-white)'),
    # Update the :root variable names
    ('--void: #3a1020', '--dark-burgundy: #3a1020'),
    ('--navy: #4A1828', '--burgundy: #4A1828'),
    ('--gold: #7DB547', '--green: #7DB547'),
    ('--gold2: #7DB547', '--deep-green: #5A8C2E'),
    ('--cream: #f8f6f0', '--warm-white: #f8f6f0'),
    ('--ink: #f8f6f0', '--mid-burgundy: #7A2E42'),
    ('--ink2: rgba(74,24,40,0.65)', ''),
    ('--navy-mid: #7A2E42', ''),
]

for old, new in replacements:
    html = html.replace(old, new)

with open('team-restyled.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! team-restyled.html created.")
