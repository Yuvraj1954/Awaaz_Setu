/*********************************
 GLOBAL STATE & VOICE FIXES
**********************************/
let currentLanguage = 'en';
let recognition;
let isListening = false;
let paused = false;

// CRITICAL VOICE FIX: Clear queue before speaking
function speakText(text, language) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel(); // Clear existing speech

    const utterance = new SpeechSynthesisUtterance(text);
    const voices = window.speechSynthesis.getVoices();

    if (language === 'hi') {
        const hindiVoice = voices.find(v => v.lang === 'hi-IN' || v.name.includes('Hindi'));
        if (hindiVoice) utterance.voice = hindiVoice;
        utterance.lang = 'hi-IN';
    } else {
        const englishVoice = voices.find(v => v.lang === 'en-IN' || v.name.includes('Google US English'));
        if (englishVoice) utterance.voice = englishVoice;
        utterance.lang = 'en-IN';
    }

    utterance.rate = 0.95;
    setTimeout(() => { window.speechSynthesis.speak(utterance); }, 50); // Small delay for browser stability
}

// --- SPEECH RECOGNITION SETUP ---
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    
    recognition.onstart = () => {
        isListening = true;
        document.querySelector('.mic-circle').style.background = '#ef4444';
        document.getElementById('mic-label').textContent = "Listening...";
    };

    recognition.onresult = (event) => {
        document.getElementById('user-input').value = event.results[0][0].transcript;
    };

    recognition.onend = () => {
        isListening = false;
        document.querySelector('.mic-circle').style.background = 'var(--primary)';
        document.getElementById('mic-label').textContent = "Tap & Speak";
        if (!paused && document.getElementById('user-input').value) submitQuery();
    };
}

// --- SUBMIT QUERY TO BACKEND ---
async function submitQuery() {
    const text = document.getElementById('user-input').value.trim();
    if (!text) return;

    document.getElementById('loading').style.display = 'flex';

    try {
        const res = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, language: currentLanguage })
        });
        const data = await res.json();
        
        document.getElementById('loading').style.display = 'none';
        document.getElementById('response-text').textContent = data.response;
        document.getElementById('response-section').style.display = 'block';
        
        speakText(data.response, currentLanguage); // Trigger voice response
    } catch (err) {
        document.getElementById('loading').style.display = 'none';
        console.error("Fetch error:", err);
    }
}

// --- LANGUAGE BUTTONS FIX ---
document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.onclick = () => {
        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentLanguage = btn.dataset.lang;
        
        // Sync recognition language
        if (recognition) recognition.lang = currentLanguage === 'hi' ? 'hi-IN' : 'en-IN';
    };
});

// --- MIC BUTTON ---
document.getElementById('mic-button').onclick = () => {
    if (!recognition) return alert("Use Chrome browser.");
    paused = false;
    isListening ? recognition.stop() : recognition.start();
};

document.getElementById('pause-btn').onclick = () => {
    paused = true;
    if (recognition) recognition.stop();
    window.speechSynthesis.cancel();
};
