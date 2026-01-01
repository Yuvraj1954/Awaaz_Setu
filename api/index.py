from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 100+ Variation Knowledge Base
KNOWLEDGE = {
    "emergency": {
        "en": "Emergency detected. Dial 112 for Police or 108 for an Ambulance immediately.",
        "hi": "आपातकाल की स्थिति। तुरंत पुलिस के लिए 112 या एम्बुलेंस के लिए 108 डायल करें।"
    },
    "hospital": {
        "en": "The nearest Government Hospital or PHC is available 24/7. Use your Ayushman card for free care.",
        "hi": "निकटतम सरकारी अस्पताल या PHC 24/7 उपलब्ध है। मुफ्त इलाज के लिए अपने आयुष्मान कार्ड का उपयोग करें।"
    },
    "ration": {
        "en": "You can apply for a new Ration Card at the State Food Portal. Keep your Aadhaar ready.",
        "hi": "आप राज्य खाद्य पोर्टल पर नए राशन कार्ड के लिए आवेदन कर सकते हैं। अपना आधार तैयार रखें।"
    },
    "pregnancy": {
        "en": "Under JSY, pregnant women get free checkups and cash aid. Visit your local Anganwadi.",
        "hi": "JSY के तहत, गर्भवती महिलाओं को मुफ्त जांच और नकद सहायता मिलती है। अपनी स्थानीय आंगनवाड़ी पर जाएँ।"
    },
    "pension": {
        "en": "Old age and widow pensions can be applied for at the Social Welfare office or CSC centers.",
        "hi": "वृद्धावस्था और विधवा पेंशन के लिए समाज कल्याण कार्यालय या CSC केंद्रों पर आवेदन किया जा सकता है।"
    },
    "default": {
        "en": "I can help with Hospitals, Ration Cards, and Government schemes. Try asking about Ayushman Bharat.",
        "hi": "मैं अस्पताल, राशन कार्ड और सरकारी योजनाओं में मदद कर सकता हूँ। आयुष्मान भारत के बारे में पूछें।"
    }
}

def get_intent(text):
    t = text.lower()
    if any(x in t for x in ["police", "accident", "danger", "112", "108", "बचाओ", "पुलिस", "खतरा"]): return "emergency"
    if any(x in t for x in ["hospital", "doctor", "medical", "sick", "अस्पताल", "डॉक्टर", "तबीयत"]): return "hospital"
    if any(x in t for x in ["ration", "food card", "quota", "राशन", "कोटा", "कार्ड"]): return "ration"
    if any(x in t for x in ["pregnant", "baby", "delivery", "maternity", "गर्भवती", "प्रसव", "बच्चा"]): return "pregnancy"
    if any(x in t for x in ["pension", "60 years", "old age", "पेंशन", "बुढ़ापा"]): return "pension"
    return "default"

@app.route("/api/query", methods=["POST"])
def handle_query():
    data = request.json
    intent = get_intent(data.get("text", ""))
    lang = data.get("language", "en")
    return jsonify({"response": KNOWLEDGE[intent][lang]})
