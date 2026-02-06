import os

chapters_dir = r'c:\Users\krish\OneDrive\Desktop\app22\chapters'
files = [f for f in os.listdir(chapters_dir) if f.startswith('chapter') and f.endswith('.html')]

skip_files = ['chapter1.html', 'chapter2.html', 'chapter3.html']

controls_head = """    <link rel="stylesheet" href="../styles.css">
    <script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
    <script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
    <style>
        .chapter-controls { position: fixed; top: 20px; right: 20px; display: flex; gap: 15px; z-index: 1000; }
        .chapter-controls button { background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); border-radius: 50%; width: 45px; height: 45px; cursor: pointer; font-size: 1.3rem; backdrop-filter: blur(10px); transition: all 0.3s ease; color: var(--primary); }
        .chapter-controls button:hover { background: rgba(255,255,255,0.1); transform: scale(1.1); }
    </style>
</head>

<body>
    <div class="chapter-controls">
        <button id="warp-btn" onclick="toggleInterstellar()" title="Interstellar Mode"><ion-icon name="rocket-outline"></ion-icon></button>
        <button id="music-btn" onclick="toggleMusic()" title="Toggle Music"><ion-icon name="musical-notes-outline"></ion-icon></button>
    </div>
    <audio id="bg-music" loop><source src="../music.mp3" type="audio/mpeg"></audio>"""

script_tag = '    <script src="../script.js"></script>\n</body>'

for filename in files:
    if filename in skip_files:
        continue
    
    filepath = os.path.join(chapters_dir, filename)
    
    # Try different encodings
    content = None
    for enc in ['utf-8', 'cp1252', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        print(f"Failed to read {filename}")
        continue
    
    # 1. Add CSS, IonIcons, Style, and Controls to head
    if '</head>' in content and '<body>' in content:
        content = content.replace('</head>', controls_head)
        content = content.replace('<body>', '', 1) 
    
    # 2. Add script.js at the end
    if '</body>' in content and '../script.js' not in content:
        content = content.replace('</body>', script_tag)
    
    # Always write back as UTF-8
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated remaining chapter files.")
