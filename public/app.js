let currentLanguage = 'en';
let recognition;
let isListening = false;

const translations = {
    en: { title: 'AwaazSetu', micLabel: 'Ready to Listen', listening: 'Listening...', insights: 'Assistant Insights' },
    hi: { title: 'आवाज़सेतु', micLabel: 'सुनने के लिए तैयार', listening: 'सुन रहा हूँ...', insights: 'सहायक अंतर्दृष्टि' }
};

// --- VISUAL FEEDBACK ENGINE ---
function updateMicUI(active) {
    const circle = document.querySelector('.inner-circle');
    const label = document.getElementById('mic-label');
    if (active) {
        circle.style.transform = 'scale(1.25)';
        circle.style.boxShadow = '0 0 70px #10b981';
        label.textContent = translations[currentLanguage].listening;
    } else {
        circle.style.transform = 'scale(1)';
        circle.style.boxShadow = '0 0 50px rgba(79, 70, 229, 0.5)';
        label.textContent = translations[currentLanguage].micLabel;
    }
}

// --- SPEECH RECOGNITION ---
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    
    recognition.onstart = () => { isListening = true; updateMicUI(true); };
    
    recognition.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        document.getElementById('user-input').value = transcript;
    };
    
    recognition.onend = () => {
        isListening = false;
        updateMicUI(false);
        if (document.getElementById('user-input').value) submitQuery();
    };
}

// --- DATA COMMUNICATION ---
async function submitQuery() {
    const text = document.getElementById('user-input').value;
    if (!text) return;
    
    document.getElementById('loading').style.display = 'flex';
    saveToHistory(text);

    try {
        const res = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, language: currentLanguage })
        });
        const data = await res.json();
        
        displayResponse(data.response);
    } catch (err) {
        console.error("Connection Failed:", err);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function displayResponse(msg) {
    document.getElementById('response-text').textContent = msg;
    document.getElementById('response-section').style.display = 'block';
    speak(msg);
}

function speak(text) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = currentLanguage === 'hi' ? 'hi-IN' : 'en-IN';
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
}

// --- SIDEBAR HISTORY ---
function saveToHistory(text) {
    const container = document.getElementById('history-list');
    const item = document.createElement('div');
    item.className = 'history-item';
    item.textContent = text.length > 25 ? text.substring(0, 25) + "..." : text;
    item.onclick = () => { 
        document.getElementById('user-input').value = text; 
        submitQuery(); 
    };
    container.prepend(item);
}

// --- INTERACTION HANDLERS ---
document.getElementById('mic-button').onclick = () => {
    if (isListening) { recognition.stop(); } 
    else { 
        if (!recognition) return alert("Please use Google Chrome for voice features.");
        recognition.lang = currentLanguage === 'hi' ? 'hi-IN' : 'en-IN';
        recognition.start(); 
    }
};

document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.onclick = () => {
        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentLanguage = btn.dataset.lang;
        document.getElementById('app-title').textContent = translations[currentLanguage].title;
        document.getElementById('mic-label').textContent = translations[currentLanguage].micLabel;
    };
});

document.getElementById('new-query-btn').onclick = () => {
    document.getElementById('response-section').style.display = 'none';
    document.getElementById('user-input').value = '';
};
