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
            'ration_card': "राशन कार्ड के लिए आप अपने पास के सरकारी राशन दफ्तर चले जाइए। वहाँ अपना आधार कार्ड, पते का सबूत और फोटो जमा करना होगा।",
            'pension': "बुढ़ापा पेंशन के लिए आप पंचायत या नगर निगम दफ्तर जाकर पता करें। साथ में अपनी उम्र और कमाई का सर्टिफिकेट जरूर ले जाएं।",
            'ayushman_bharat': "आयुष्मान योजना में आप 5 लाख रुपये तक का मुफ्त इलाज पा सकते हैं। अपना आधार कार्ड लेकर किसी भी सरकारी अस्पताल में जाकर अपनी जाँच करवाएं।",
            'housing': "घर बनाने की योजना के लिए आप ऑनलाइन पीएम आवास पोर्टल पर भर सकते हैं या अपने ब्लॉक दफ्तर में जमीन के कागज लेकर मिलें।",
            'birth_certificate': "बच्चे के जन्म का सर्टिफिकेट बनवाने के लिए 21 दिन के अंदर नगर निगम दफ्तर जाएं। अस्पताल की पर्ची और माँ-बाप का पहचान पत्र साथ रखें।",
            'voter_id': "वोटर आईडी बनवाने के लिए आप ऑनलाइन फॉर्म भरें या तहसील दफ्तर चले जाएं। आपकी उम्र कम से कम 18 साल होनी चाहिए।",
            'aadhar': "नया आधार बनवाने के लिए पास के आधार केंद्र पर जाएँ। वहाँ आपकी फोटो और उंगलियों के निशान लिए जाएंगे और कार्ड डाक से घर आ जाएगा।",
            'default': "मैं आयुष्मान भारत, राशन कार्ड, पेंशन और घर की योजना के बारे में बता सकता हूँ। आपको किस बारे में जानकारी चाहिए?"
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
            'fever': "अगर आपको बुखार है तो खूब आराम करें और पानी पिएं। अगर 3 दिन तक बुखार न उतरे तो पास के डॉक्टर को जरूर दिखाएं।",
            'cough_cold': "खांसी या जुकाम में गर्म पानी पिएं और आराम करें। अगर एक हफ्ते तक ठीक न हों तो सरकारी अस्पताल जाकर डॉक्टर से मिलें।",
            'hospital_guidance': "अगर कोई इमरजेंसी है तो तुरंत बड़े सरकारी अस्पताल जाएं। आम जाँच के लिए आप सुबह-सुबह पास के स्वास्थ्य केंद्र जा सकते हैं।",
            'stomach_pain': "हल्के पेट दर्द में खिचड़ी जैसा हल्का खाना खाएं और साफ पानी पिएं। अगर दर्द बहुत तेज हो तो फौरन डॉक्टर के पास जाएं।",
            'vaccination': "सरकारी सेंटरों पर टीके मुफ्त लगाए जाते हैं। बच्चे के जन्म का कागज और अपना हेल्थ कार्ड साथ लेकर ही जाएं।",
            'pregnancy': "गर्भवती माताएं जाँच और मुफ्त दवाइयों के लिए जितनी जल्दी हो सके अपने पास के स्वास्थ्य केंद्र में नाम लिखवा लें।",
            'default': "मैं बुखार, खांसी, जुकाम और अस्पताल जाने के बारे में बता सकता हूँ। आपको क्या तकलीफ हो रही है?"
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
