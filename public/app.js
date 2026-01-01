let currentLanguage = 'en';
let recognition;
let isListening = false;

// History Logic
function addToHistory(text) {
    const container = document.getElementById('history-list');
    if (!container) return;
    const item = document.createElement('div');
    item.style = "background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; font-size: 0.85rem; margin-top: 12px; cursor: pointer; border: 1px solid rgba(255,255,255,0.1);";
    item.textContent = text.length > 20 ? text.substring(0, 20) + "..." : text;
    item.onclick = () => { document.getElementById('user-input').value = text; submitQuery(); };
    container.prepend(item);
}

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.onstart = () => { isListening = true; document.querySelector('.inner-circle').style.transform = 'scale(1.2)'; };
    recognition.onresult = (e) => { document.getElementById('user-input').value = e.results[0][0].transcript; };
    recognition.onend = () => { isListening = false; document.querySelector('.inner-circle').style.transform = 'scale(1)'; if (document.getElementById('user-input').value) submitQuery(); };
}

async function submitQuery() {
    const text = document.getElementById('user-input').value;
    if (!text) return;
    document.getElementById('loading').style.display = 'flex';
    addToHistory(text);

    const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, language: currentLanguage })
    });
    const data = await res.json();
    document.getElementById('loading').style.display = 'none';
    document.getElementById('response-text').textContent = data.response;
    document.getElementById('response-section').style.display = 'block';
    
    // Auto Speech
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(data.response);
    u.lang = currentLanguage === 'hi' ? 'hi-IN' : 'en-IN';
    window.speechSynthesis.speak(u);
}

document.getElementById('mic-button').onclick = () => { 
    recognition.lang = currentLanguage === 'hi' ? 'hi-IN' : 'en-IN';
    isListening ? recognition.stop() : recognition.start(); 
};

document.querySelectorAll('.lang-btn').forEach(b => b.onclick = () => {
    document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
    b.classList.add('active');
    currentLanguage = b.dataset.lang;
});
