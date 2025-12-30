import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

# Firebase setup
# For demo purposes, we will use a local JSON file if provided, 
# or a mock for truly "offline" demo if secrets aren't set yet.
# In a real scenario, the user would provide the service account JSON via Replit Secrets.
db = None
try:
    firebase_creds_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
    if firebase_creds_json:
        creds_dict = json.loads(firebase_creds_json)
        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
except Exception as e:
    print(f"Firebase initialization error: {e}")

# Hardcoded data for truly offline demo/fallback
MOCK_DATA = [
    {"service": "government", "language": "en", "intent": "ayushman_bharat", "response": "Ayushman Bharat provides free healthcare. Check your eligibility at any government hospital with your Aadhaar card."},
    {"service": "government", "language": "en", "intent": "ration_card", "response": "You can apply for a ration card at your local food office. Bring your ID, address proof, and photos."},
    {"service": "government", "language": "en", "intent": "pension", "response": "For the old age pension, you should visit the Panchayat or Municipal office with your age and income certificates."},
    {"service": "government", "language": "hi", "intent": "ayushman_bharat", "response": "आयुष्मान योजना में आप 5 लाख रुपये तक का मुफ्त इलाज पा सकते हैं। अपना आधार कार्ड लेकर किसी भी सरकारी अस्पताल में जाकर अपनी जाँच करवाएं।"},
    {"service": "government", "language": "hi", "intent": "ration_card", "response": "राशन कार्ड के लिए आप अपने पास के सरकारी राशन दफ्तर चले जाइए। वहाँ अपना आधार कार्ड, पते का सबूत और फोटो जमा करना होगा।"},
    {"service": "government", "language": "hi", "intent": "pension", "response": "बुढ़ापा पेंशन के लिए आप पंचायत या नगर निगम दफ्तर जाकर पता करें। साथ में अपनी उम्र और कमाई का सर्टिफिकेट जरूर ले जाएं।"},
    {"service": "healthcare", "language": "en", "intent": "fever", "response": "If you have a fever, rest and drink plenty of fluids. If it stays high for 3 days, please see a doctor."},
    {"service": "healthcare", "language": "en", "intent": "cough_cold", "response": "For a cough or cold, warm water and rest usually help. If symptoms persist for a week, visit a health center."},
    {"service": "healthcare", "language": "en", "intent": "hospital_guidance", "response": "For emergencies, go to the nearest government hospital. For general checkups, visit the primary health center in the morning."},
    {"service": "healthcare", "language": "hi", "intent": "fever", "response": "अगर आपको बुखार है तो खूब आराम करें और पानी पिएं। अगर 3 दिन तक बुखार न उतरे तो पास के डॉक्टर को जरूर दिखाएं।"},
    {"service": "healthcare", "language": "hi", "intent": "cough_cold", "response": "खांसी या जुकाम में गर्म पानी पिएं और आराम करें। अगर एक हफ्ते तक ठीक न हों तो सरकारी अस्पताल जाकर डॉक्टर से मिलें।"},
    {"service": "healthcare", "hi": "hospital_guidance", "response": "अगर कोई इमरजेंसी है तो तुरंत बड़े सरकारी अस्पताल जाएं। आम जाँच के लिए आप सुबह-सुबह पास के स्वास्थ्य केंद्र जा सकते हैं।"}
]

def get_response_from_db(service, language, intent):
    """Fetches response from Firebase/Mock data."""
    if db:
        try:
            docs = db.collection("responses").where("service", "==", service).where("language", "==", language).where("intent", "==", intent).stream()
            for doc in docs:
                return doc.to_dict().get("response")
            
            # Fallback to default
            docs_default = db.collection("responses").where("service", "==", service).where("language", "==", language).where("intent", "==", "default").stream()
            for doc in docs_default:
                return doc.to_dict().get("response")
        except Exception as e:
            print(f"Firebase error: {e}")

    # Fallback to mock data for demo/offline
    for item in MOCK_DATA:
        if item.get("service") == service and item.get("language") == language and item.get("intent") == intent:
            return item.get("response")
    
    # Ultimate fallback
    return "I'm sorry, I couldn't find that information." if language == 'en' else "माफ़ कीजिये, मुझे वह जानकारी नहीं मिली।"

def detect_intent(text_input, service):
    """Analyzes the user's text to find the most relevant intent based on keywords."""
    text_input = text_input.lower()
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
    if service in keywords:
        for intent, words in keywords[service].items():
            for word in words:
                if word in text_input:
                    return intent
    return 'default'

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/query', methods=['POST'])
def process_query():
    try:
        data = request.json
        text_input = data.get('text', '')
        service = data.get('service', 'government')
        language = data.get('language', 'en')
        if not text_input.strip():
            return jsonify({'response': 'Please type your question.' if language == 'en' else 'कृपया अपना सवाल लिखें।', 'success': True})
        intent = detect_intent(text_input, service)
        response = get_response_from_db(service, language, intent)
        return jsonify({'response': response, 'success': True, 'intent': intent})
    except Exception as e:
        return jsonify({'response': 'Sorry, something went wrong. Please try again.' if language == 'en' else 'क्षमा करें, कुछ गलत हुआ। कृपया पुनः प्रयास करें।', 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
