from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

RESPONSES = {
    'government': {
        'en': {
            'ration_card': "You can apply for a ration card at your local food office. Bring your ID, address proof, and photos.",
            'pension': "For the old age pension, you should visit the Panchayat or Municipal office with your age and income certificates.",
            'ayushman_bharat': "Ayushman Bharat provides free healthcare. Check your eligibility at any government hospital with your Aadhaar card.",
            'housing': "For the housing scheme, apply through the PM Awas Yojana portal or visit your local block office with your land papers.",
            'birth_certificate': "Register births at your local municipal office within 21 days. You'll need the hospital record and parents' IDs.",
            'voter_id': "You can register for a voter ID online or at the Tehsildar's office. You must be at least 18 years old.",
            'aadhar': "Visit an Aadhaar center for a new card. They will take your fingerprints and photo. It usually arrives by post.",
            'default': "I can help with Ayushman Bharat, ration cards, pensions, housing, and other certificates. What do you need?"
        },
        'hi': {
            'ration_card': "राशन कार्ड के लिए खाद्य विभाग के कार्यालय जाएं। अपना पहचान पत्र, पता और फोटो साथ ले जाएं।",
            'pension': "वृद्धावस्था पेंशन के लिए पंचायत या नगर निगम कार्यालय जाएं। उम्र और आय का प्रमाण पत्र साथ रखें।",
            'ayushman_bharat': "आयुष्मान भारत में मुफ्त इलाज मिलता है। अपना आधार कार्ड लेकर सरकारी अस्पताल में अपनी पात्रता जांचें।",
            'housing': "आवास योजना के लिए पीएम आवास पोर्टल पर आवेदन करें या अपने ब्लॉक कार्यालय में जमीन के कागजात लेकर जाएं।",
            'birth_certificate': "जन्म के 21 दिन के भीतर नगर निगम में पंजीकरण कराएं। अस्पताल की पर्ची और माता-पिता का आईडी चाहिए होगा।",
            'voter_id': "वोटर आईडी के लिए ऑनलाइन या तहसील कार्यालय में आवेदन करें। आपकी उम्र 18 साल होनी चाहिए।",
            'aadhar': "नए आधार के लिए आधार केंद्र जाएं। वहां आपकी फोटो और उंगलियों के निशान लिए जाएंगे। कार्ड डाक से आएगा।",
            'default': "मैं आयुष्मान भारत, राशन कार्ड, पेंशन और आवास योजना में आपकी मदद कर सकता हूं। आपको क्या जानकारी चाहिए?"
        }
    },
    'healthcare': {
        'en': {
            'fever': "If you have a fever, rest and drink plenty of fluids. If it stays high for 3 days, please see a doctor.",
            'cough_cold': "For a cough or cold, warm water and rest usually help. If symptoms persist for a week, visit a health center.",
            'hospital_guidance': "For emergencies, go to the nearest government hospital. For general checkups, visit the primary health center in the morning.",
            'stomach_pain': "For mild stomach pain, eat light food and drink clean water. If the pain is sharp or constant, see a doctor immediately.",
            'vaccination': "Vaccinations are free at government centers. Bring the child's birth record and your health card.",
            'pregnancy': "Pregnant women should register at the local health center early for checkups and free supplements.",
            'default': "I can guide you on fever, cough, cold, and how to find a hospital. Please tell me your concern."
        },
        'hi': {
            'fever': "बुखार होने पर आराम करें और खूब पानी पिएं। अगर 3 दिन तक बुखार न उतरे, तो डॉक्टर को जरूर दिखाएं।",
            'cough_cold': "सर्दी-खांसी में गर्म पानी और आराम से फायदा होता है। अगर एक हफ्ते तक सुधार न हो, तो स्वास्थ्य केंद्र जाएं।",
            'hospital_guidance': "आपात स्थिति में नजदीकी सरकारी अस्पताल जाएं। सामान्य जांच के लिए सुबह प्राथमिक स्वास्थ्य केंद्र जा सकते हैं।",
            'stomach_pain': "हल्के पेट दर्द में हल्का खाना खाएं और साफ पानी पिएं। तेज या लगातार दर्द होने पर तुरंत डॉक्टर से मिलें।",
            'vaccination': "सरकारी केंद्रों पर टीके मुफ्त लगते हैं। बच्चे का जन्म रिकॉर्ड और अपना स्वास्थ्य कार्ड साथ लाएं।",
            'pregnancy': "गर्भवती महिलाएं जांच और मुफ्त दवाइयों के लिए जल्द ही स्वास्थ्य केंद्र में पंजीकरण कराएं।",
            'default': "मैं बुखार, सर्दी-खांसी और अस्पताल की जानकारी में आपकी मदद कर सकता हूं। आपको क्या तकलीफ है?"
        }
    }
}

def detect_intent(text, service, language):
    """
    Analyzes the user's text to find the most relevant intent based on keywords.
    It loops through predefined categories and returns the first matching key.
    """
    text = text.lower()

    # Define keyword maps for intent detection
    keywords = {
        'government': {
            'ayushman_bharat': ['ayushman', 'bharat', 'gold card', 'health card', 'आयुष्मान', 'भारत'],
            'ration_card': ['ration', 'card', 'food', 'राशन', 'कार्ड'],
            'pension': ['pension', 'old age', 'बुढ़ापा', 'पेंशन'],
            'housing': ['house', 'housing', 'home', 'awas', 'yojana', 'घर', 'आवास'],
            'birth_certificate': ['birth', 'certificate', 'जन्म', 'प्रमाण'],
            'voter_id': ['voter', 'election', 'id', 'वोटर', 'पहचान पत्र'],
            'aadhar': ['aadhar', 'aadhaar', 'आधार']
        },
        'healthcare': {
            'fever': ['fever', 'temperature', 'bukhar', 'बुखार', 'तापमान'],
            'cough_cold': ['cough', 'cold', 'flu', 'khasi', 'sardi', 'खांसी', 'जुकाम', 'सर्दी'],
            'hospital_guidance': ['hospital', 'doctor', 'clinic', 'checkup', 'अस्पताल', 'डॉक्टर', 'क्लीनिक'],
            'stomach_pain': ['stomach', 'pain', 'belly', 'pet', 'dard', 'पेट', 'दर्द'],
            'vaccination': ['vaccine', 'vaccination', 'injection', 'tika', 'टीका', 'टीकाकरण'],
            'pregnancy': ['pregnant', 'pregnancy', 'baby', 'delivery', 'गर्भवती', 'बच्चा']
        }
    }

    # Search for keywords in the input text
    if service in keywords:
        for intent, words in keywords[service].items():
            for word in words:
                if word in text:
                    return intent

    return 'default'

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/query', methods=['POST'])
def process_query():
    try:
        data = request.json
        text = data.get('text', '')
        service = data.get('service', 'government')
        language = data.get('language', 'en')

        if not text.strip():
            return jsonify({
                'response': 'Please type your question.' if language == 'en' else 'कृपया अपना सवाल लिखें।',
                'success': True
            })

        intent = detect_intent(text, service, language)
        response = RESPONSES.get(service, {}).get(language, {}).get(intent,
                   RESPONSES[service][language]['default'])

        return jsonify({
            'response': response,
            'success': True,
            'intent': intent
        })
    except Exception as e:
        return jsonify({
            'response': 'Sorry, something went wrong. Please try again.' if language == 'en'
                       else 'क्षमा करें, कुछ गलत हुआ। कृपया पुनः प्रयास करें।',
            'success': False
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
