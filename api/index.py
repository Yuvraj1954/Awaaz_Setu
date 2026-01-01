from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

KNOWLEDGE = {
    "ayushman": {
        "en": "Ayushman Bharat provides up to 5 lakh rupees of free health cover per family per year. Check eligibility at any PMJAY hospital.",
        "hi": "आयुष्मान भारत प्रति परिवार 5 लाख रुपये तक का मुफ्त स्वास्थ्य कवर प्रदान करता है। PMJAY अस्पताल में जांच करें।"
    },
    "emergency": {
        "en": "Emergency detected. Dial 112 for Police or 108 for an Ambulance immediately.",
        "hi": "आपातकाल की स्थिति। तुरंत पुलिस के लिए 112 या एम्बुलेंस के लिए 108 डायल करें।"
    },
    "hospital": {
        "en": "The nearest Government Hospital is available 24/7. Use your Ayushman card for free care.",
        "hi": "निकटतम सरकारी अस्पताल 24/7 उपलब्ध है। मुफ्त इलाज के लिए आयुष्मान कार्ड का उपयोग करें।"
    },
    "default": {
        "en": "I can help with Hospitals, Ration Cards, and Government schemes. Try asking about Ayushman Bharat.",
        "hi": "मैं अस्पताल, राशन कार्ड और सरकारी योजनाओं में मदद कर सकता हूँ। आयुष्मान भारत के बारे में पूछें।"
    }
}

def get_intent(text):
    t = text.lower()
    if any(x in t for x in ["ayushman", "bharat", "pmjay", "आयुष्मान", "भारत"]): return "ayushman"
    if any(x in t for x in ["police", "112", "108", "emergency", "पुलिस"]): return "emergency"
    if any(x in t for x in ["hospital", "doctor", "medical", "अस्पताल", "डॉक्टर"]): return "hospital"
    return "default"

@app.route("/api/query", methods=["POST"])
def handle_query():
    data = request.json
    intent = get_intent(data.get("text", ""))
    lang = data.get("language", "en")
    return jsonify({"response": KNOWLEDGE[intent][lang]})
