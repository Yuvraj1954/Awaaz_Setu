from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

RESPONSES = {
    'government': {
        'en': {
            'ration_card': "To get a ration card, visit your nearest ration office with ID proof and address proof. You will need Aadhaar card and a passport photo.",
            'pension': "For old age pension, you must be 60 years or older. Visit your local panchayat office with age proof and income certificate.",
            'birth_certificate': "For birth certificate, go to municipal office within 21 days of birth. Bring hospital birth report and parents ID proof.",
            'voter_id': "To get voter ID, visit election office with age proof, address proof and photo. You must be 18 years or older.",
            'aadhar': "For Aadhaar card, visit nearest Aadhaar center with address proof. Biometric data will be collected. Card comes in 90 days.",
            'default': "I can help with: ration card, pension, birth certificate, voter ID, and Aadhaar card. What do you need help with?"
        },
        'hi': {
            'ration_card': "राशन कार्ड के लिए, अपने नजदीकी राशन कार्यालय जाएं। आईडी प्रूफ और एड्रेस प्रूफ साथ लेकर जाएं। आधार कार्ड और फोटो चाहिए।",
            'pension': "वृद्धावस्था पेंशन के लिए, आपकी उम्र 60 साल या उससे ज्यादा होनी चाहिए। स्थानीय पंचायत कार्यालय जाएं।",
            'birth_certificate': "जन्म प्रमाण पत्र के लिए, नगर निगम कार्यालय जाएं। जन्म के 21 दिन के अंदर। अस्पताल की रिपोर्ट और माता-पिता का आईडी लेकर जाएं।",
            'voter_id': "वोटर आईडी के लिए, चुनाव कार्यालय जाएं। उम्र प्रूफ, एड्रेस प्रूफ और फोटो चाहिए। आपकी उम्र 18 साल या उससे ज्यादा होनी चाहिए।",
            'aadhar': "आधार कार्ड के लिए, नजदीकी आधार केंद्र जाएं। एड्रेस प्रूफ साथ लेकर जाएं। बायोमेट्रिक डेटा लिया जाएगा। कार्ड 90 दिन में आएगा।",
            'default': "मैं मदद कर सकता हूं: राशन कार्ड, पेंशन, जन्म प्रमाण पत्र, वोटर आईडी, आधार कार्ड। आपको किसमें मदद चाहिए?"
        }
    },
    'healthcare': {
        'en': {
            'fever': "For fever, rest and drink plenty of water. Take paracetamol if fever is high. If fever lasts more than 3 days, visit nearest health center.",
            'cold_cough': "For cold and cough, drink warm water and rest well. Avoid cold drinks. If problem continues for 5 days, see a doctor.",
            'stomach_pain': "For stomach pain, drink clean boiled water. Eat light food like rice and dal. If pain is severe or continues, visit doctor immediately.",
            'vaccination': "For child vaccination, visit nearest Anganwadi or health center. Bring birth certificate. Vaccines are free. Keep vaccination card safe.",
            'pregnancy': "For pregnancy care, register at health center in first 3 months. Get regular checkups. Eat nutritious food. Iron tablets are given free.",
            'default': "I can help with: fever, cold and cough, stomach pain, vaccination, and pregnancy care. What is your health concern?"
        },
        'hi': {
            'fever': "बुखार के लिए, आराम करें और खूब पानी पिएं। तेज बुखार हो तो पैरासिटामोल लें। 3 दिन से ज्यादा बुखार हो तो हेल्थ सेंटर जाएं।",
            'cold_cough': "सर्दी और खांसी के लिए, गर्म पानी पिएं और आराम करें। ठंडी चीजें ना खाएं। 5 दिन से ज्यादा समस्या हो तो डॉक्टर को दिखाएं।",
            'stomach_pain': "पेट दर्द के लिए, साफ उबला पानी पिएं। हल्का खाना जैसे चावल और दाल खाएं। तेज दर्द हो तो तुरंत डॉक्टर के पास जाएं।",
            'vaccination': "बच्चे के टीकाकरण के लिए, नजदीकी आंगनवाड़ी या हेल्थ सेंटर जाएं। जन्म प्रमाण पत्र साथ लेकर जाएं। टीके मुफ्त हैं।",
            'pregnancy': "गर्भावस्था देखभाल के लिए, पहले 3 महीने में हेल्थ सेंटर में रजिस्टर करें। नियमित जांच कराएं। पौष्टिक खाना खाएं। आयरन की गोलियां मुफ्त मिलती हैं।",
            'default': "मैं मदद कर सकता हूं: बुखार, सर्दी और खांसी, पेट दर्द, टीकाकरण, गर्भावस्था देखभाल। आपकी स्वास्थ्य समस्या क्या है?"
        }
    }
}

def detect_intent(text, service, language):
    text = text.lower()

    keywords = {
        'government': {
            'ration_card': ['ration', 'card', 'राशन', 'कार्ड'],
            'pension': ['pension', 'पेंशन', 'old age', 'वृद्धावस्था'],
            'birth_certificate': ['birth', 'certificate', 'जन्म', 'प्रमाण'],
            'voter_id': ['voter', 'election', 'वोटर', 'चुनाव'],
            'aadhar': ['aadhar', 'aadhaar', 'आधार']
        },
        'healthcare': {
            'fever': ['fever', 'bukhar', 'बुखार', 'temperature'],
            'cold_cough': ['cold', 'cough', 'सर्दी', 'खांसी', 'khasi'],
            'stomach_pain': ['stomach', 'pain', 'पेट', 'दर्द', 'pet'],
            'vaccination': ['vaccine', 'vaccination', 'टीका', 'tika', 'टीकाकरण'],
            'pregnancy': ['pregnancy', 'pregnant', 'गर्भावस्था', 'garbhavastha']
        }
    }

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
