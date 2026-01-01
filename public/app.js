let currentLanguage = 'en';
let recognition;

// --- UI UPDATES ---
function updateFullUI() {
    renderGrid();
    refreshRecentQueries();
}

function renderGrid() {
    const grid = document.getElementById('command-grid');
    if (!grid) return;
    grid.innerHTML = "";
    const prompts = currentLanguage === 'en' ? ["Hi", "Help", "Ayushman Bharat", "Ration Card", "PM Kisan"] : ["नमस्ते", "मदद", "आयुष्मान भारत", "राशन कार्ड", "पीएम किसान"];
    prompts.forEach(text => {
        const chip = document.createElement('div');
        chip.className = "suggest-chip";
        chip.textContent = text;
        chip.onclick = () => { document.getElementById('user-input').value = text; submitQuery(); };
        grid.appendChild(chip);
    });
}

// --- SIDEBAR RECENT QUERIES (LIMIT 5) ---
async function refreshRecentQueries() {
    try {
        const res = await fetch('/api/history');
        const data = await res.json();
        const container = document.getElementById('history-list');
        if (!container) return;
        container.innerHTML = data.slice(0, 5).map(item => `
            <div class="history-item" onclick="document.getElementById('user-input').value='${item.text}'; submitQuery();">
                ${item.text.length > 20 ? item.text.substring(0, 20) + '...' : item.text}
            </div>
        `).join('');
    } catch (e) { console.error("Sidebar update failed", e); }
}

// --- MIC ANIMATION & RECOGNITION ---
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.onstart = () => { 
        document.getElementById('mic-container').classList.add('pulse-active'); 
        document.getElementById('mic-label').textContent = "Listening...";
    };
    recognition.onend = () => { 
        document.getElementById('mic-container').classList.remove('pulse-active');
        document.getElementById('mic-label').textContent = "Tap to Speak";
        if (document.getElementById('user-input').value) submitQuery(); 
    };
    recognition.onresult = (e) => { document.getElementById('user-input').value = e.results[0][0].transcript; };
}

document.getElementById('mic-button').onclick = () => { recognition.start(); };

// --- SUBMIT QUERY ---
async function submitQuery() {
    const text = document.getElementById('user-input').value;
    if (!text) return;
    const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, language: currentLanguage })
    });
    const data = await res.json();
    document.getElementById('response-text').textContent = data.response;
    document.getElementById('response-section').style.display = 'block';
    refreshRecentQueries();
}

window.onload = () => {
    updateFullUI();
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentLanguage = btn.dataset.lang;
            updateFullUI();
        };
    });
};
