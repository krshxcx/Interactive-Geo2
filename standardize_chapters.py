import os
import re

chapters_dir = r'c:\Users\krish\OneDrive\Desktop\app22\chapters'
files = [f for f in os.listdir(chapters_dir) if f.startswith('chapter') and f.endswith('.html')]

template_start = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../styles.css">
    <script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
    <script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
    <style>
        .chapter-controls {{ position: fixed; top: 20px; right: 20px; display: flex; gap: 15px; z-index: 1000; }}
        .chapter-controls button {{ background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); border-radius: 50%; width: 45px; height: 45px; cursor: pointer; font-size: 1.3rem; backdrop-filter: blur(10px); transition: all 0.3s ease; color: var(--primary); }}
        .chapter-controls button:hover {{ background: rgba(255,255,255,0.1); transform: scale(1.1); }}
    </style>
</head>
<body>
    <div class="chapter-controls">
        <button id="warp-btn" onclick="toggleInterstellar()" title="Interstellar Mode"><ion-icon name="rocket-outline"></ion-icon></button>
        <button id="music-btn" onclick="toggleMusic()" title="Toggle Music"><ion-icon name="musical-notes-outline"></ion-icon></button>
    </div>
    <audio id="bg-music" loop><source src="../music.mp3" type="audio/mpeg"></audio>
    <div id="chapter-content">"""

for filename in files:
    filepath = os.path.join(chapters_dir, filename)
    
    content = None
    for enc in ['utf-8', 'cp1252', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    if content is None: continue
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Geography Chapter"
    
    # Replace everything from start to <div id="chapter-content">
    # Handle both existing and missing tags
    new_content = re.sub(r'^.*?<div id="chapter-content">', template_start.format(title=title), content, flags=re.DOTALL | re.IGNORECASE)
    
    # Ensure script tag is at the end
    script_pattern = r'<script src="\.\./script\.js"></script>'
    if not re.search(script_pattern, new_content):
        new_content = re.sub(r'</div>\s*</body>', r'    </div>\n    <script src="../script.js"></script>\n</body>', new_content, flags=re.IGNORECASE)
    
    # Write back as UTF-8
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"Standardized all {len(files)} chapter files.")
