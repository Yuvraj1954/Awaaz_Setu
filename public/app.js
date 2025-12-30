/*********************************
 GLOBAL STATE
**********************************/
let currentLanguage = 'en';
let currentService = 'auto';
let recognition;
let isListening = false;
let paused = false;

/*********************************
 TRANSLATIONS
**********************************/
speechSynthesis.onvoiceschanged = () => {};

const translations = {
    en: {
        title: 'AwaazSetu',
        subtitle: 'Your Voice Bridge to Services',
        tagline: 'Speak in Hindi or English to get help with government and healthcare services.',
        micLabel: 'Tap & Speak',
        listening: 'Listening...',
        tryAsking: 'Try asking:',
        inputLabel: 'How can we help you?',
        inputPlaceholder: 'Type your question here...',
        submit: 'Ask Question',
        cancel: 'Cancel',
        responseTitle: 'Response',
        newQuery: 'Ask Another Question',
        loading: 'Finding information...'
    },
    hi: {
        title: 'आवाज़सेतु',
        subtitle: 'सेवाओं के लिए आपका आवाज़ पुल',
        tagline: 'सरकारी और स्वास्थ्य सेवाओं में मदद के लिए हिंदी या अंग्रेजी में बोलें।',
        micLabel: 'बोलने के लिए टैप करें',
        listening: 'सुन रहा हूँ...',
        tryAsking: 'पूछने का प्रयास करें:',
        inputLabel: 'हम आपकी कैसे मदद कर सकते हैं?',
        inputPlaceholder: 'अपना सवाल यहाँ लिखें...',
        submit: 'सवाल पूछें',
        cancel: 'रद्द करें',
        responseTitle: 'जवाब',
        newQuery: 'दूसरा सवाल पूछें',
        loading: 'जानकारी ढूंढ रहे हैं...'
    }
};

/*********************************
 SPEECH RECOGNITION
**********************************/
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        if (paused) return;
        isListening = true;
        document.querySelector('.mic-circle').style.background = '#ef4444';
        document.getElementById('mic-label').textContent =
            translations[currentLanguage].listening;
    };

    recognition.onresult = (event) => {
        if (paused) return;
        document.getElementById('user-input').value =
            event.results[0][0].transcript;
    };

    recognition.onend = () => {
        isListening = false;
        document.querySelector('.mic-circle').style.background = 'var(--primary)';
        document.getElementById('mic-label').textContent =
            translations[currentLanguage].micLabel;

        if (paused) return;
        const text = document.getElementById('user-input').value.trim();
        if (text) submitQuery();
    };

    recognition.onerror = () => {
        isListening = false;
        document.querySelector('.mic-circle').style.background = 'var(--primary)';
    };
}

/*********************************
 TEXT TO SPEECH (IMPROVED ENGLISH)
**********************************/
function speakText(text, language) {
    if (!('speechSynthesis' in window)) return;

    speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const voices = speechSynthesis.getVoices();

    if (language === 'en') {
        const voice =
            voices.find(v => v.name.includes('Google') && v.lang.startsWith('en')) ||
            voices.find(v => v.lang === 'en-IN') ||
            voices.find(v => v.lang.startsWith('en'));

        if (voice) utterance.voice = voice;
        utterance.lang = 'en-IN';
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
    } else {
        const voice = voices.find(v => v.lang === 'hi-IN');
        if (voice) utterance.voice = voice;
        utterance.lang = 'hi-IN';
        utterance.rate = 0.95;
    }

    speechSynthesis.speak(utterance);
}

/*********************************
 LANGUAGE UPDATE
**********************************/
function updateLanguage() {
    const t = translations[currentLanguage];
    document.getElementById('app-title').textContent = t.title;
    document.getElementById('app-subtitle').textContent = t.subtitle;
    document.getElementById('app-tagline').textContent = t.tagline;
    document.getElementById('mic-label').textContent = t.micLabel;
    document.getElementById('try-asking-label').textContent = t.tryAsking;
    document.getElementById('input-label').textContent = t.inputLabel;
    document.getElementById('user-input').placeholder = t.inputPlaceholder;
    document.getElementById('submit-text').textContent = t.submit;
    document.getElementById('cancel-text').textContent = t.cancel;
    document.getElementById('response-title').textContent = t.responseTitle;
    document.getElementById('new-query-text').textContent = t.newQuery;
    document.getElementById('loading-text').textContent = t.loading;

    if (recognition) {
        recognition.lang = currentLanguage === 'hi' ? 'hi-IN' : 'en-IN';
    }
}

/*********************************
 LANGUAGE BUTTONS (FIXED)
**********************************/
document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        paused = false;
        document.querySelectorAll('.lang-btn').forEach(b =>
            b.classList.remove('active')
        );
        btn.classList.add('active');
        currentLanguage = btn.dataset.lang;
        updateLanguage();
        loadRandomPrompts(); // ✅ KEY FIX
    });
});

/*********************************
 MIC BUTTON
**********************************/
document.getElementById('mic-button').addEventListener('click', () => {
    if (!recognition) return alert('Please use Chrome for voice input.');
    paused = false;
    recognition.lang = currentLanguage === 'hi' ? 'hi-IN' : 'en-IN';
    isListening ? recognition.stop() : recognition.start();
});

/*********************************
 SUBMIT QUERY
**********************************/
async function submitQuery() {
    if (paused) return;
    const text = document.getElementById('user-input').value.trim();
    if (!text) return;

    document.getElementById('loading').style.display = 'flex';

    try {
        const res = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text,
                service: currentService,
                language: currentLanguage
            })
        });

        const data = await res.json();
        document.getElementById('loading').style.display = 'none';
        document.getElementById('response-text').textContent = data.response;
        document.getElementById('response-section').style.display = 'block';
        speakText(data.response, currentLanguage);

    } catch {
        document.getElementById('loading').style.display = 'none';
        alert('Server error. Please try again.');
    }
}

/*********************************
 PAUSE BUTTON
**********************************/
function forceStopAll() {
    paused = true;
    if (recognition && isListening) recognition.stop();
    if ('speechSynthesis' in window) speechSynthesis.cancel();
    document.getElementById('loading').style.display = 'none';
}

document.getElementById('pause-btn').addEventListener('click', forceStopAll);

/*********************************
 PERMANENT PROMPTS (BILINGUAL)
**********************************/
const promptPool = [
    {
        ui_en: "PM Awas Yojana",
        ui_hi: "पीएम आवास योजना",
        send: "PM Awas Yojana"
    },
    {
        ui_en: "Women helpline",
        ui_hi: "महिला हेल्पलाइन",
        send: "Women helpline"
    },
    {
        ui_en: "Emergency number",
        ui_hi: "आपातकालीन नंबर",
        send: "Emergency number"
    },
    {
        ui_en: "Ration card kaise banaye",
        ui_hi: "राशन कार्ड कैसे बनवाएं",
        send: "राशन कार्ड कैसे बनवाएं"
    },
    {
        ui_en: "Ayushman Bharat",
        ui_hi: "आयुष्मान भारत",
        send: "Ayushman Bharat"
    }
];

function loadRandomPrompts() {
    const items = document.querySelectorAll('.prompt-item');

    items.forEach((el, i) => {
        if (!promptPool[i]) return;

        el.textContent =
            currentLanguage === 'hi'
                ? promptPool[i].ui_hi
                : promptPool[i].ui_en;

        el.onclick = () => {
            document.getElementById('user-input').value =
                promptPool[i].send;
            submitQuery();
        };
    });
}

/*********************************
 ASK ANOTHER QUESTION
**********************************/
document.getElementById('new-query-btn').addEventListener('click', () => {
    paused = false;
    if ('speechSynthesis' in window) speechSynthesis.cancel();
    document.getElementById('response-section').style.display = 'none';
    document.getElementById('user-input').value = '';
});

/*********************************
 INIT
**********************************/
window.addEventListener('load', () => {
    paused = false;
    updateLanguage();
    loadRandomPrompts();
});
