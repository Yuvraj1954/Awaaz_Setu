let currentLanguage = 'en';
let recognition;
let isListening = false;

const translations = { 
    en: { 
        micLabel: 'Tap to Speak', 
        listening: 'Listening...', 
        status: 'Bridge Active', 
        stopBtn: 'Stop Listening', 
        askAnother: 'Ask Another', 
        respHead: 'Assistant Response' 
    }, 
    hi: { 
        micLabel: 'बोलने के लिए टैप करें', 
        listening: 'सुन रहा हूँ...', 
        status: 'ब्रिज सक्रिय है', 
        stopBtn: 'सुनना बंद करें', 
        askAnother: 'दूसरा पूछें', 
        respHead: 'सहायक की प्रतिक्रिया' 
    } 
};

function setUiState(listening) {
    const container = document.getElementById('mic-container');
    if (listening) {
        container.classList.add('pulse-active');
    } else {
        container.classList.remove('pulse-active');
    }
}

function updateUiLanguage() {
    const t = translations[currentLanguage];
    document.getElementById('mic-label').textContent = t.micLabel;
    document.getElementById('status-text').textContent = t.status;
    document.getElementById('pause-btn').textContent = t.stopBtn;
    const askBtn = document.getElementById('new-query-btn');
    if(askBtn) askBtn.textContent = t.askAnother;
}

async function refreshSidebar() {
    try {
        const res = await fetch('/api/history');
        const history = await res.json();
        const container = document.getElementById('history-list');
        if (!container) return;
        
        container.innerHTML = ""; 
        history.slice(0, 5).forEach(item => {
            const div = document.createElement('div'); 
            div.className = "history-item"; 
            div.textContent = item.text.length > 25 ? item.text.substring(0, 25) + "..." : item.text;
            div.onclick = () => { 
                document.getElementById('user-input').value = item.text; 
                submitQuery(); 
            };
            container.appendChild(div);
        });
    } catch (e) { 
        console.error("Sidebar refresh failed:", e); 
    }
}

// --- UPDATED NATURAL VOICE ENGINE ---
function speakResponse(text, lang) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const voices = window.speechSynthesis.getVoices();
    
    if (lang === 'hi') {
        utterance.lang = 'hi-IN';
        utterance.voice = voices.find(v => v.lang === 'hi-IN' && v.name.includes('Google')) || 
                         voices.find(v => v.lang === 'hi-IN');
        utterance.rate = 1.0; 
    } else {
        utterance.lang = 'en-IN';
        // Priority: Neural/Natural sounding voices for Indian English
        const indianVoice = voices.find(v => v.name.includes('Neural') && v.lang === 'en-IN') || 
                           voices.find(v => v.lang === 'en-IN' && v.name.includes('Google')) ||
                           voices.find(v => v.lang === 'en-IN');
        
        utterance.voice = indianVoice || voices.find(v => v.lang === 'en-GB');
        
        // FIXED: Increased rate to 1.05 to sound less robotic and more energetic
        utterance.rate = 1.05; 
        utterance.pitch = 1.0;
    }
    window.speechSynthesis.speak(utterance);
}

window.onload = () => { 
    refreshSidebar(); 
    document.querySelectorAll('.lang-btn').forEach(btn => { 
        btn.onclick = () => { 
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active')); 
            btn.classList.add('active'); 
            currentLanguage = btn.getAttribute('data-lang'); 
            updateUiLanguage();
        }; 
    });
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
    }
};

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.onstart = () => { 
        isListening = true;
        setUiState(true); 
        document.getElementById('mic-label').textContent = translations[currentLanguage].listening; 
    };
    recognition.onresult = (e) => { 
        document.getElementById('user-input').value = e.results[0][0].transcript; 
    };
    recognition.onend = () => { 
        isListening = false;
        setUiState(false); 
        document.getElementById('mic-label').textContent = translations[currentLanguage].micLabel; 
        if (document.getElementById('user-input').value) submitQuery(); 
    };
}

async function submitQuery() {
    const text = document.getElementById('user-input').value;
    if (!text) return;
    try {
        const res = await fetch('/api/query', { 
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify({ text, language: currentLanguage }) 
        });
        const data = await res.json();
        const responseSection = document.getElementById('response-section');
        document.getElementById('response-text').textContent = data.response;
        responseSection.style.display = 'block';
        speakResponse(data.response, currentLanguage);
        refreshSidebar();
    } catch (e) { 
        console.error("Query failed:", e); 
        setUiState(false); 
    }
}

document.getElementById('mic-button').onclick = () => { 
    if (!recognition) return alert("Speech recognition not supported.");
    recognition.lang = currentLanguage === 'hi' ? 'hi-IN' : 'en-IN'; 
    isListening ? recognition.stop() : recognition.start(); 
};

document.getElementById('history-btn').onclick = () => { window.location.href = 'history.html'; };
document.getElementById('new-query-btn').onclick = () => { 
    document.getElementById('response-section').style.display = 'none'; 
    document.getElementById('user-input').value = ''; 
    window.speechSynthesis.cancel();
};
document.getElementById('pause-btn').onclick = () => { 
    window.speechSynthesis.cancel(); 
    if (recognition) recognition.stop(); 
    setUiState(false); 
};
