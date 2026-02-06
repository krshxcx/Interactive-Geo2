
/* 
    ANTIGRAVITY ENGINE v2.0
    Optimized: Reduced particle count, smoother transitions, enhanced Wiki-Hover.
*/

// --- CONFIGURATION ---
const chapters = [
    { id: 1, title: "Geography as a Discipline", subtitle: "Definition & Scope", icon: "compass", color: "#FF6B6B" },
    { id: 2, title: "Origin & Evolution", subtitle: "Nebula to Big Bang", icon: "planet", color: "#FFE66D" },
    { id: 3, title: "Interior of Earth", subtitle: "Crust, Mantle, Core", icon: "layers", color: "#4ECDC4" },
    { id: 4, title: "Oceans & Continents", subtitle: "Drift & Tectonics", icon: "earth", color: "#96CEB4" },
    { id: 5, title: "Minerals & Rocks", subtitle: "Building Blocks", icon: "cube", color: "#FF8C42" },
    { id: 6, title: "Geomorphic Processes", subtitle: "Earth Forces", icon: "construct", color: "#D9534F" },
    { id: 7, title: "Landforms & Evolution", subtitle: "Sculpting the Surface", icon: "image", color: "#A8DADC" },
    { id: 8, title: "Atmosphere Structure", subtitle: "Gases & Layers", icon: "cloud", color: "#45B7D1" },
    { id: 9, title: "Solar Radiation", subtitle: "Heat Balance", icon: "sunny", color: "#F9A825" },
    { id: 10, title: "Atmospheric Circulation", subtitle: "Winds & Pressure", icon: "shuffle", color: "#6A89CC" },
    { id: 11, title: "Water in Atmosphere", subtitle: "Clouds & Rain", icon: "water", color: "#82CCDD" },
    { id: 12, title: "World Climate", subtitle: "Köppen & Climate Change", icon: "thermometer", color: "#E55039" },
    { id: 13, title: "Water (Oceans)", subtitle: "The Blue Realm", icon: "boat", color: "#1E3799" },
    { id: 14, title: "Ocean Movements", subtitle: "Currents & Tides", icon: "pulse", color: "#38ADA9" },
    { id: 15, title: "Life on Earth", subtitle: "Biosphere & Ecology", icon: "leaf", color: "#78E08F" },
    { id: 16, title: "Biodiversity", subtitle: "Conservation", icon: "flower", color: "#B8E994" }
];

// --- STATE ---
let isDetailViewActive = false;

// --- ELEMENTS ---
const homeView = document.getElementById('home-view');
const detailView = document.getElementById('detail-view');
const timelineContainer = document.getElementById('timeline');

// --- HOVER CARD (Created once, reused) ---
const hoverCard = document.createElement('div');
hoverCard.className = 'hover-card';
document.body.appendChild(hoverCard);

// --- INIT ---
document.addEventListener('DOMContentLoaded', () => {
    initStars();
    renderTimeline();

    // Parallax (optimized: throttled)
    let ticking = false;
    document.addEventListener('mousemove', (e) => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                handleParallax(e);
                ticking = false;
            });
            ticking = true;
        }
    });

    // Keyboard navigation (FIXED: Backspace goes to home, not browser back)
    document.addEventListener('keydown', (e) => {
        // Only handle backspace if we're NOT in a text input/textarea
        const activeEl = document.activeElement;
        const isTyping = activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA' || activeEl.isContentEditable);

        if (e.key === 'Backspace' && !isTyping) {
            if (isDetailViewActive) {
                e.preventDefault();
                e.stopPropagation();
                showHome();
                return false;
            }
        }
        if (e.key === 'Escape' && isDetailViewActive) {
            e.preventDefault();
            showHome();
        }
    }, true); // Use capture phase for higher priority

    // Prevent browser back on backspace globally when in detail view
    window.addEventListener('popstate', (e) => {
        if (isDetailViewActive) {
            e.preventDefault();
            history.pushState(null, null, location.href);
            showHome();
        }
    });

    // Push initial state for popstate handling
    history.pushState(null, null, location.href);
});

// --- NAVIGATION LOGIC ---
window.openChapterPage = async function (id) {
    const chapter = chapters.find(c => c.id === id);
    if (!chapter) return;

    isDetailViewActive = true;

    // 1. Update Header Info
    document.getElementById('detail-title').innerText = chapter.title;
    document.getElementById('detail-subtitle').innerText = `CHAPTER ${id} - ${chapter.subtitle}`;
    const iconContainer = document.getElementById('detail-icon');
    iconContainer.setAttribute('name', chapter.icon);
    iconContainer.style.color = chapter.color;

    // 2. Fetch Content
    const contentContainer = document.getElementById('detail-content');
    contentContainer.innerHTML = '<div class="loading-state"><ion-icon name="sync-outline"></ion-icon> Loading...</div>';

    // Transition UI (optimized: use will-change)
    homeView.style.willChange = 'transform, opacity';
    detailView.style.willChange = 'transform, opacity';

    homeView.classList.add('exit-left');
    detailView.classList.remove('hidden');

    // Slight delay to allow CSS transition to start visible state
    requestAnimationFrame(() => {
        detailView.classList.add('active');
    });

    try {
        const response = await fetch(`chapters/chapter${id}.html`);
        if (!response.ok) throw new Error("Data stream interrupted.");

        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        // Extract content - INTELLIGENT PARSER
        let content = doc.getElementById('chapter-content') ||
            doc.querySelector('.page-container') ||
            doc.body;

        if (content && content.innerHTML.trim().length > 0) {
            contentContainer.innerHTML = content.innerHTML;
            attachWikiHover(); // Attach Wiki Hover Listeners
        } else {
            contentContainer.innerHTML = `<div class="content-block"><h3>Module Offline</h3><p>Signal received but no visual data found.</p></div>`;
        }

    } catch (e) {
        console.error(e);
        contentContainer.innerHTML = `<div class="content-block"><h3>Communication Broken</h3><p>${e.message}</p></div>`;
    }

    // Clean up will-change after transition
    setTimeout(() => {
        homeView.style.willChange = 'auto';
        detailView.style.willChange = 'auto';
    }, 800);
};

window.showHome = function () {
    isDetailViewActive = false;
    detailView.classList.remove('active');

    setTimeout(() => {
        homeView.classList.remove('exit-left');
        detailView.classList.add('hidden');
    }, 500);
};

// --- DOM RENDERING ---
function renderTimeline() {
    timelineContainer.innerHTML = '<div class="timeline-spine"></div>';

    chapters.forEach(chapter => {
        const card = document.createElement('div');
        card.className = 'chapter-card';
        card.onclick = () => openChapterPage(chapter.id);

        const paddedId = chapter.id < 10 ? `0${chapter.id}` : chapter.id;

        card.innerHTML = `
            <div class="timeline-dot"></div>
            <div class="card-glass" data-tilt>
                <div class="chapter-num">${paddedId}</div>
                <div style="font-size: 3rem; color: ${chapter.color}; margin-bottom: 20px;">
                    <ion-icon name="${chapter.icon}"></ion-icon>
                </div>
                <h2>${chapter.title}</h2>
                <p>${chapter.subtitle}</p>
            </div>
        `;

        timelineContainer.appendChild(card);
    });

    initObserver();
}

function initObserver() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.15 });

    document.querySelectorAll('.chapter-card').forEach(el => observer.observe(el));
}

// --- VISUAL EFFECTS (OPTIMIZED) ---

// 1. Dynamic Stars with Shooting Stars
function initStars() {
    const starField = document.createElement('div');
    starField.className = 'star-field';
    document.body.appendChild(starField);

    const fragment = document.createDocumentFragment();

    // Create 50 twinkling stars
    for (let i = 0; i < 50; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        const size = Math.random() * 3 + 1;
        star.style.cssText = `
            position: absolute;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            width: ${size}px;
            height: ${size}px;
            background: white;
            border-radius: 50%;
            opacity: ${Math.random() * 0.5 + 0.5};
            animation: twinkle ${Math.random() * 3 + 2}s ease-in-out infinite;
            animation-delay: ${Math.random() * 3}s;
            box-shadow: 0 0 ${size * 2}px rgba(255,255,255,0.5);
        `;
        fragment.appendChild(star);
    }

    starField.appendChild(fragment);
}

// 2. Parallax & Tilt (Optimized)
function handleParallax(e) {
    const x = (window.innerWidth - e.pageX * 2) / 150;
    const y = (window.innerHeight - e.pageY * 2) / 150;

    // Move background stars slowly
    const starField = document.querySelector('.star-field');
    if (starField) {
        starField.style.transform = `translate3d(${x * 0.5}px, ${y * 0.5}px, 0)`;
    }

    // Move hero elements
    const planet = document.querySelector('.planet-system');
    if (planet) {
        planet.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    }
}

// --- MUSIC PLAYER ---
function toggleMusic() {
    const audio = document.getElementById('bg-music');
    const btn = document.getElementById('music-btn');

    if (!audio || !btn) return;

    if (audio.paused) {
        audio.play().then(() => {
            btn.classList.add('playing');
            btn.innerHTML = '<ion-icon name="volume-high"></ion-icon>';
        }).catch(e => {
            console.log("Audio playback failed (user interaction needed first):", e);
            alert("Please interact with the document first to play audio.");
        });
    } else {
        audio.pause();
        btn.classList.remove('playing');
        btn.innerHTML = '<ion-icon name="musical-notes-outline"></ion-icon>';
    }
}

// --- WIKI HOVER ENGINE ---
function attachWikiHover() {
    const triggers = document.querySelectorAll('.wiki-term');

    triggers.forEach(trigger => {
        // Make the term a clickable link if it has a data-link
        const link = trigger.getAttribute('data-link');
        if (link) {
            trigger.style.cursor = 'pointer';
            trigger.addEventListener('click', (e) => {
                window.open(link, '_blank');
            });
        }

        trigger.addEventListener('mouseenter', (e) => {
            const title = trigger.getAttribute('data-title') || 'Definition';
            const summary = trigger.getAttribute('data-summary') || '';
            const img = trigger.getAttribute('data-image') || '';

            let html = '';
            if (img) html += `<img src="${img}" class="hover-visual" alt="${title}">`;
            html += `
                <div class="hover-content">
                    <div class="hover-title"><ion-icon name="book-outline"></ion-icon> ${title}</div>
                    <div class="hover-summary">${summary}</div>
                    ${link ? `<a href="${link}" target="_blank" class="hover-link" onclick="event.stopPropagation();">Read on Wikipedia <ion-icon name="open-outline"></ion-icon></a>` : ''}
                </div>
            `;

            hoverCard.innerHTML = html;
            hoverCard.classList.add('active');

            positionCard(e, trigger);
        });

        trigger.addEventListener('mousemove', (e) => {
            positionCard(e, trigger);
        });

        trigger.addEventListener('mouseleave', () => {
            hoverCard.classList.remove('active');
        });
    });
}

function positionCard(e, trigger) {
    const triggerRect = trigger.getBoundingClientRect();
    const cardWidth = 320;
    const cardHeight = 180;

    // Calculate available space
    const spaceRight = window.innerWidth - triggerRect.right;
    const spaceBottom = window.innerHeight - triggerRect.bottom;

    let left = e.clientX + 15;
    let top = e.clientY + 15;

    // Flip to left if too close to right edge
    if (spaceRight < cardWidth + 30) {
        left = e.clientX - cardWidth - 15;
    }

    // Flip up if too close to bottom
    if (spaceBottom < cardHeight + 30) {
        top = e.clientY - cardHeight - 15;
    }

    // Ensure minimum bounds
    left = Math.max(10, left);
    top = Math.max(10, top);

    hoverCard.style.left = `${left}px`;
    hoverCard.style.top = `${top}px`;
}

// --- INTERSTELLAR MODE ---
let interstellarIntervals = [];

function toggleInterstellar() {
    const isActive = document.body.classList.toggle('interstellar-mode');
    const warpBtn = document.getElementById('warp-btn');

    if (isActive) {
        warpBtn.style.color = 'var(--accent)';
        warpBtn.innerHTML = '<ion-icon name="rocket"></ion-icon>';

        const starField = document.querySelector('.star-field') || document.body;
        const planetSystem = document.querySelector('.planet-system');

        // 1. Slow Falling Stars (Very slow, 15-30s)
        for (let i = 0; i < 10; i++) {
            const star = document.createElement('div');
            star.className = 'shooting-star';
            star.style.left = (Math.random() * 120 - 10) + '%';
            star.style.animationDuration = (Math.random() * 15 + 15) + 's';
            star.style.animationDelay = (Math.random() * 15) + 's';
            starField.appendChild(star);
        }

        // 2. Soft Nebula Glows
        const colors = ['#4A90E2', '#9013FE'];
        for (let i = 0; i < 2; i++) {
            const nebula = document.createElement('div');
            nebula.className = 'nebula';
            nebula.style.backgroundColor = colors[i];
            nebula.style.top = (i === 0 ? '10%' : '60%');
            nebula.style.left = (i === 0 ? '20%' : '50%');
            document.body.appendChild(nebula);
        }

        // 3. Cute UFOs (Slow roaming)
        for (let i = 0; i < 3; i++) {
            const ufo = document.createElement('div');
            ufo.className = 'ufo';
            ufo.style.top = (Math.random() * 50 + 20) + '%';
            ufo.style.left = (Math.random() * 60 + 20) + '%';
            ufo.style.animation = `roam ${(Math.random() * 25 + 20)}s infinite ease-in-out`;
            starField.appendChild(ufo);
        }

        // 4. Just 2 Slowly Roaming Satellites
        for (let i = 0; i < 2; i++) {
            const sat = document.createElement('div');
            sat.className = 'cute-satellite';
            sat.style.top = (20 + i * 30) + '%';
            sat.style.left = (30 + i * 25) + '%';
            sat.style.animation = `sat-roam ${(40 + i * 20)}s infinite ease-in-out`;
            document.body.appendChild(sat);
        }

        // 5. Just 1 Slow Cloud
        const cloud = document.createElement('div');
        cloud.className = 'cute-cloud';
        cloud.style.top = '15%';
        cloud.style.left = '-200px';
        cloud.style.transition = 'left 100s linear';
        document.body.appendChild(cloud);
        setTimeout(() => { cloud.style.left = '110vw'; }, 200);

        // 6. Earth Orbiting Satellite
        if (planetSystem) {
            const earthSatWrapper = document.createElement('div');
            earthSatWrapper.id = 'earth-sat-orbiter';
            const earthSat = document.createElement('div');
            earthSat.className = 'cute-satellite';
            earthSat.style.top = '0';
            earthSat.style.left = '50%';
            earthSatWrapper.appendChild(earthSat);
            planetSystem.appendChild(earthSatWrapper);
        }

        // 7. Slow Rocket
        const rocket = document.createElement('div');
        rocket.className = 'cute-rocket';
        rocket.innerHTML = '<div class="rocket-flame"></div>';
        document.body.appendChild(rocket);

    } else {
        warpBtn.style.color = 'var(--primary)';
        warpBtn.innerHTML = '<ion-icon name="rocket-outline"></ion-icon>';
        interstellarIntervals.forEach(clearInterval);
        interstellarIntervals = [];
        const cleanup = [
            '.shooting-star', '.nebula', '.cute-cloud', '.ufo',
            '#earth-sat-orbiter', '.cute-satellite', '.cute-rocket'
        ];
        cleanup.forEach(selector => document.querySelectorAll(selector).forEach(el => el.remove()));
    }
}

