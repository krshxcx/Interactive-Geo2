"""
Enhance all 16 chapter HTML files with:
- Bookmark button in chapter controls
- Key Takeaways section
- Chapter Navigation (Prev/Next)
- Hero banner images
- Quick Facts callouts
"""
import re
import os

CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), 'chapters')

chapters_data = [
    {"id": 1,  "title": "Geography as a Discipline", "subtitle": "Definition & Scope"},
    {"id": 2,  "title": "Origin & Evolution", "subtitle": "Nebula to Big Bang"},
    {"id": 3,  "title": "Interior of Earth", "subtitle": "Crust, Mantle, Core"},
    {"id": 4,  "title": "Oceans & Continents", "subtitle": "Drift & Tectonics"},
    {"id": 5,  "title": "Minerals & Rocks", "subtitle": "Building Blocks"},
    {"id": 6,  "title": "Geomorphic Processes", "subtitle": "Earth Forces"},
    {"id": 7,  "title": "Landforms & Evolution", "subtitle": "Sculpting the Surface"},
    {"id": 8,  "title": "Atmosphere Structure", "subtitle": "Gases & Layers"},
    {"id": 9,  "title": "Solar Radiation", "subtitle": "Heat Balance"},
    {"id": 10, "title": "Atmospheric Circulation", "subtitle": "Winds & Pressure"},
    {"id": 11, "title": "Water in Atmosphere", "subtitle": "Clouds & Rain"},
    {"id": 12, "title": "World Climate", "subtitle": "Köppen & Climate Change"},
    {"id": 13, "title": "Water (Oceans)", "subtitle": "The Blue Realm"},
    {"id": 14, "title": "Ocean Movements", "subtitle": "Currents & Tides"},
    {"id": 15, "title": "Life on Earth", "subtitle": "Biosphere & Ecology"},
    {"id": 16, "title": "Biodiversity", "subtitle": "Conservation"},
]

# Key takeaways per chapter
takeaways = {
    1: [
        "Geography is both a natural and social science — a 'discipline of synthesis'",
        "Coined by <strong>Eratosthenes</strong> (276-194 BC): <em>Geo</em> = Earth + <em>Graphos</em> = Description",
        "Two major approaches: <strong>Systematic</strong> (Humboldt) vs <strong>Regional</strong> (Ritter)",
        "Modern tools: GIS, GPS, Remote Sensing revolutionize spatial analysis",
    ],
    2: [
        "Universe originated ~<strong>13.8 billion years ago</strong> (Big Bang Theory)",
        "Earth formed ~<strong>4.6 billion years ago</strong> from solar nebula accretion",
        "Early atmosphere had no free oxygen — it was dominated by H₂, He, NH₃, CH₄",
        "Moon formed from a Mars-sized impact (<strong>Giant Impact Hypothesis</strong>)",
    ],
    3: [
        "Earth's interior is known through <strong>seismic waves</strong> (P-waves and S-waves)",
        "Three layers: <strong>Crust</strong> (5-70 km), <strong>Mantle</strong> (2900 km), <strong>Core</strong> (3500 km radius)",
        "The <strong>Mohorovičić Discontinuity</strong> separates crust from mantle",
        "S-waves cannot pass through the outer core → it must be <strong>liquid</strong>",
    ],
    4: [
        "Wegener's <strong>Continental Drift</strong> (1912): Continents were once joined as <strong>Pangaea</strong>",
        "Plate Tectonics explains earthquakes, volcanoes, and mountain building",
        "Three types of plate boundaries: <strong>Divergent</strong>, <strong>Convergent</strong>, <strong>Transform</strong>",
        "Sea-floor spreading proved by magnetic stripe symmetry along mid-ocean ridges",
    ],
    5: [
        "Minerals are naturally occurring, inorganic, solid with a definite chemical composition",
        "Three rock types: <strong>Igneous</strong>, <strong>Sedimentary</strong>, <strong>Metamorphic</strong>",
        "The <strong>Rock Cycle</strong> shows continuous transformation between rock types",
        "<strong>Feldspar</strong> is the most abundant mineral group in Earth's crust",
    ],
    6: [
        "Geomorphic processes are either <strong>endogenic</strong> (internal) or <strong>exogenic</strong> (external)",
        "Endogenic forces: <strong>Volcanism</strong>, <strong>Diastrophism</strong>, <strong>Earthquakes</strong>",
        "Exogenic forces: <strong>Weathering</strong>, <strong>Erosion</strong>, <strong>Mass Wasting</strong>",
        "Weathering is in-situ; erosion involves transport by wind, water, ice, or gravity",
    ],
    7: [
        "Landforms are shaped by running water, wind, glaciers, and waves",
        "River stages: <strong>Youth</strong> (V-valleys), <strong>Mature</strong> (meanders), <strong>Old</strong> (floodplains, deltas)",
        "Glacial landforms: <strong>Cirques</strong>, <strong>U-valleys</strong>, <strong>Moraines</strong>, <strong>Drumlins</strong>",
        "Karst topography forms in limestone regions: sinkholes, caves, stalactites",
    ],
    8: [
        "Atmosphere composition: <strong>N₂ (78%)</strong>, <strong>O₂ (21%)</strong>, <strong>Ar (0.93%)</strong>, CO₂ (0.04%)",
        "Five layers: <strong>Troposphere</strong>, Stratosphere, Mesosphere, Thermosphere, Exosphere",
        "Temperature decreases at <strong>6.5°C per km</strong> in the troposphere (Normal Lapse Rate)",
        "The <strong>Ozone layer</strong> in the stratosphere absorbs harmful UV radiation",
    ],
    9: [
        "Earth receives solar energy as <strong>shortwave radiation</strong>; emits <strong>longwave (infrared)</strong>",
        "<strong>Albedo</strong> = % of solar radiation reflected (fresh snow ≈ 80-90%, water ≈ 5-10%)",
        "Insolation varies with latitude, season, and length of day",
        "<strong>Heat budget</strong>: incoming solar = outgoing terrestrial radiation (balanced over time)",
    ],
    10: [
        "Winds flow from <strong>high pressure</strong> to <strong>low pressure</strong> areas",
        "<strong>Coriolis Effect</strong>: deflects winds right in NH, left in SH",
        "Three wind cells: <strong>Hadley</strong>, <strong>Ferrel</strong>, <strong>Polar</strong>",
        "<strong>Jet Streams</strong> are fast upper-atmosphere winds influencing weather patterns",
    ],
    11: [
        "Water exists in atmosphere as <strong>water vapor</strong>, clouds, and precipitation",
        "<strong>Dew point</strong>: temperature at which air becomes saturated (100% RH)",
        "Cloud classification: <strong>Cirrus</strong> (high), <strong>Stratus</strong> (layered), <strong>Cumulus</strong> (puffy)",
        "Types of rainfall: <strong>Convectional</strong>, <strong>Orographic</strong>, <strong>Cyclonic/Frontal</strong>",
    ],
    12: [
        "<strong>Köppen Classification</strong>: 5 major climate groups (A, B, C, D, E) + Highland (H)",
        "Classification based on <strong>temperature</strong> and <strong>precipitation</strong> patterns",
        "Without the greenhouse effect, Earth would be <strong>-18°C</strong> instead of <strong>+15°C</strong>",
        "Key protocols: <strong>Kyoto (1997)</strong> and <strong>Paris Agreement (2015)</strong>",
    ],
    13: [
        "Oceans cover <strong>71%</strong> of Earth's surface and hold <strong>97%</strong> of all water",
        "Ocean floor: <strong>Continental Shelf</strong> → Slope → Rise → <strong>Abyssal Plain</strong> → Trenches",
        "Average ocean temperature: <strong>~17°C</strong>; salinity: <strong>35‰ (parts per thousand)</strong>",
        "Temperature and salinity decrease with depth; density increases",
    ],
    14: [
        "Three types of ocean movements: <strong>Waves</strong>, <strong>Tides</strong>, <strong>Currents</strong>",
        "Tides are caused by <strong>gravitational pull</strong> of Moon (primary) and Sun",
        "<strong>Spring tides</strong> = Sun + Moon aligned; <strong>Neap tides</strong> = perpendicular",
        "Ocean currents redistribute heat: <strong>Gulf Stream</strong> warms Western Europe",
    ],
    15: [
        "The <strong>Biosphere</strong> = Lithosphere + Hydrosphere + Atmosphere (zone of life)",
        "<strong>Ecology</strong>: study of relationships between organisms and their environment",
        "Key terms: <strong>Habitat</strong>, <strong>Niche</strong>, <strong>Ecosystem</strong>, <strong>Biome</strong>",
        "Food chains → Food webs → <strong>Ecological pyramids</strong> (number, biomass, energy)",
    ],
    16: [
        "<strong>Biodiversity</strong> = variety of life at genetic, species, and ecosystem levels",
        "Three types: <strong>Genetic</strong> diversity, <strong>Species</strong> diversity, <strong>Ecosystem</strong> diversity",
        "Threats: <strong>Habitat loss</strong>, overexploitation, invasive species, climate change",
        "Conservation strategies: <strong>In-situ</strong> (National Parks) and <strong>Ex-situ</strong> (Zoos, Gene Banks)",
    ],
}

# Hero banner images from Wikimedia Commons
hero_images = {
    1: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/The_Earth_seen_from_Apollo_17.jpg/1200px-The_Earth_seen_from_Apollo_17.jpg",
    2: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/GalaxyNGC4414.jpg/800px-GalaxyNGC4414.jpg",
    3: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Earth-crust-cutaway-english.svg/800px-Earth-crust-cutaway-english.svg.png",
    4: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Plates_tect2_en.svg/800px-Plates_tect2_en.svg.png",
    5: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Rockcycle.jpg/800px-Rockcycle.jpg",
    6: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Geological_Processes.jpg/800px-Geological_Processes.jpg",
    7: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Grand_Canyon_view_from_Pima_Point_2010.jpg/800px-Grand_Canyon_view_from_Pima_Point_2010.jpg",
    8: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Atmosphere_layers-en.svg/800px-Atmosphere_layers-en.svg.png",
    9: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Solar_Spectrum.png/800px-Solar_Spectrum.png",
    10: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Earth_Global_Circulation_-_en.svg/800px-Earth_Global_Circulation_-_en.svg.png",
    11: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Water_cycle.png/800px-Water_cycle.png",
    12: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Koppen-Geiger_Map_KG_present.svg/1200px-Koppen-Geiger_Map_KG_present.svg.png",
    13: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Okeanos.jpg/800px-Okeanos.jpg",
    14: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Corrientes-oceanicas.png/800px-Corrientes-oceanicas.png",
    15: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Amazon_Rainforest.jpg/800px-Amazon_Rainforest.jpg",
    16: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Biodiversit%C3%A9.jpg/800px-Biodiversit%C3%A9.jpg",
}

def get_chapter_nav_html(chapter_id):
    """Generate prev/next navigation HTML"""
    prev_ch = chapters_data[chapter_id - 2] if chapter_id > 1 else None
    next_ch = chapters_data[chapter_id] if chapter_id < 16 else None
    
    nav = '<div class="chapter-nav">\n'
    
    if prev_ch:
        nav += f'    <a href="chapter{prev_ch["id"]}.html" class="prev">\n'
        nav += f'        <span class="nav-dir">← Previous</span>\n'
        nav += f'        <span class="nav-title">{prev_ch["title"]}</span>\n'
        nav += '    </a>\n'
    else:
        nav += '    <a class="prev disabled"><span class="nav-dir">← Previous</span><span class="nav-title">—</span></a>\n'
    
    if next_ch:
        nav += f'    <a href="chapter{next_ch["id"]}.html" class="next">\n'
        nav += f'        <span class="nav-dir">Next →</span>\n'
        nav += f'        <span class="nav-title">{next_ch["title"]}</span>\n'
        nav += '    </a>\n'
    else:
        nav += '    <a class="next disabled"><span class="nav-dir">Next →</span><span class="nav-title">—</span></a>\n'
    
    nav += '</div>\n'
    return nav

def get_key_takeaways_html(chapter_id):
    """Generate key takeaways card HTML"""
    items = takeaways.get(chapter_id, [])
    if not items:
        return ''
    
    html = '<div class="key-takeaways">\n'
    html += '    <h3><ion-icon name="bulb-outline"></ion-icon> Key Takeaways</h3>\n'
    html += '    <ul>\n'
    for item in items:
        html += f'        <li>{item}</li>\n'
    html += '    </ul>\n'
    html += '</div>\n'
    return html

def get_hero_banner_html(chapter_id):
    """Generate hero banner image HTML"""
    img_url = hero_images.get(chapter_id)
    if not img_url:
        return ''
    ch = chapters_data[chapter_id - 1]
    return f'<img src="{img_url}" alt="{ch["title"]}" class="chapter-hero-banner" loading="lazy">\n'

def process_chapter(chapter_id):
    filepath = os.path.join(CHAPTERS_DIR, f'chapter{chapter_id}.html')
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 1. Add bookmark button to chapter controls (if not already present)
    if 'bookmark-btn' not in content:
        bookmark_btn = (
            '        <button id="bookmark-btn" class="bookmark-btn" title="Bookmark">'
            '<ion-icon name="bookmark-outline"></ion-icon></button>\n'
        )
        # Insert after the music button
        content = content.replace(
            '        <button id="music-btn" onclick="toggleMusic()" title="Toggle Music"><ion-icon\n                name="musical-notes-outline"></ion-icon></button>',
            '        <button id="music-btn" onclick="toggleMusic()" title="Toggle Music"><ion-icon\n                name="musical-notes-outline"></ion-icon></button>\n' + bookmark_btn
        )
        modified = True
    
    # 2. Add key takeaways after the hero section
    if 'key-takeaways' not in content:
        kt_html = get_key_takeaways_html(chapter_id)
        if kt_html:
            # Insert after the first content-block (hero)
            hero_end = '            </div>\n\n            <!-- =='
            if hero_end in content:
                content = content.replace(hero_end, '            </div>\n\n' + kt_html + '\n            <!-- ==', 1)
                modified = True
    
    # 3. Add hero banner image after <article class="chapter-article">
    if 'chapter-hero-banner' not in content:
        banner_html = get_hero_banner_html(chapter_id)
        if banner_html:
            content = content.replace(
                '<article class="chapter-article">',
                '<article class="chapter-article">\n\n            ' + banner_html
            )
            modified = True
    
    # 4. Add chapter navigation before </article>
    if 'chapter-nav' not in content:
        nav_html = get_chapter_nav_html(chapter_id)
        content = content.replace(
            '        </article>',
            '\n            ' + nav_html + '\n        </article>'
        )
        modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK chapter{chapter_id}.html enhanced")
    else:
        print(f"  -- chapter{chapter_id}.html already enhanced")

if __name__ == '__main__':
    print("Enhancing chapter files...")
    for ch in chapters_data:
        process_chapter(ch['id'])
    print("\nDone! All chapters enhanced.")
