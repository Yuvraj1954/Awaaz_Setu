from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
import random

app = Flask(__name__)
CORS(app)

# --- DATABASE CONNECTION ---
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    MONGO_URI = "mongodb+srv://yuvrajk863888_db_user:aMnHBizntIPta5VX@cluster0.x4euc3w.mongodb.net/awaaz_setu_db?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URI)
    db = client['awaaz_setu_db']
    logs_collection = db['query_logs']
except Exception as e:
    print(f"MongoDB Connection Error: {e}")

# --- ROBUST KNOWLEDGE BASE ---
KNOWLEDGE = {
    "greetings": {
        "en": "Hello! I am AwaazSetu, your government service assistant. I can help you find information about health schemes, ration cards, and emergency services. How can I help you today?",
        "hi": "नमस्ते! मैं आवाज़सेतु हूँ, आपका सरकारी सेवा सहायक। मैं स्वास्थ्य योजनाओं, राशन कार्ड और आपातकालीन सेवाओं के बारे में जानकारी खोजने में आपकी मदद कर सकता हूँ।"
    },
    "help": {
        "en": "I am designed to assist with government services. You can ask: 'How to apply for a Ration Card?', 'Benefits of Ayushman Bharat', or 'Show me emergency numbers'. What would you like to know?",
        "hi": "मैं सरकारी सेवाओं में सहायता के लिए हूँ। आप पूछ सकते हैं: 'राशन कार्ड के लिए आवेदन कैसे करें?', 'आयुष्मान भारत के लाभ', या 'मुझे आपातकालीन नंबर दिखाएं'।"
    },
    "ayushman": {
        "en": "Ayushman Bharat (PM-JAY) provides free health cover of ₹5 Lakhs per family per year. It covers over 1,500 medical procedures. You can apply at any PMJAY empanelled hospital with your Aadhaar and Ration Card.",
        "hi": "आयुष्मान भारत (PM-JAY) प्रति परिवार प्रति वर्ष ₹5 लाख का मुफ्त स्वास्थ्य कवर प्रदान करता है। इसमें 1,500 से अधिक चिकित्सा प्रक्रियाएं शामिल हैं। आप अपने आधार और राशन कार्ड के साथ किसी भी PMJAY अस्पताल में आवेदन कर सकते हैं।"
    },
    "ration": {
        "en": "Ration Cards are issued by State Governments for subsidized food. To apply, visit your local Food & Supplies office or the official state portal. Key documents needed: Aadhaar, Address Proof, and Income Certificate.",
        "hi": "सब्सिडी वाले भोजन के लिए राज्य सरकारों द्वारा राशन कार्ड जारी किए जाते हैं। आवेदन करने के लिए, अपने स्थानीय खाद्य और आपूर्ति कार्यालय या आधिकारिक राज्य पोर्टल पर जाएं। आवश्यक दस्तावेज: आधार, पते का प्रमाण और आय प्रमाण पत्र।"
    },
    "emergency": {
        "en": "In case of emergency, stay calm. Dial 112 for All-in-one Emergency, 100 for Police, 108 for Medical Ambulance, and 101 for Fire services. Help is available 24/7.",
        "hi": "आपातकाल की स्थिति में शांत रहें। सभी आपात स्थितियों के लिए 112, पुलिस के लिए 100, मेडिकल एम्बुलेंस के लिए 108 और अग्निशमन सेवाओं के लिए 101 डायल करें।"
    },
    "hospital": {
        "en": "Government hospitals provide free treatment for emergency cases. For specialized care, you can use your Ayushman Bharat card at private hospitals listed under the PMJAY scheme. Please visit the nearest District Hospital for general checkups.",
        "hi": "सरकारी अस्पताल आपातकालीन मामलों के लिए मुफ्त इलाज प्रदान करते हैं। विशेष देखभाल के लिए, आप PMJAY योजना के तहत सूचीबद्ध निजी अस्पतालों में अपने आयुष्मान भारत कार्ड का उपयोग कर सकते हैं।"
    }
}

# --- DYNAMIC FALLBACKS ---
FALLBACKS = {
    "en": [
        "I'm not quite sure about that. Try asking about Ayushman Bharat or Ration Card processes.",
        "I don't have that information in my database yet. You can ask for 'Help' to see what I can do!",
        "Could you please repeat that? I specialize in government schemes and emergency services."
    ],
    "hi": [
        "मुझे इसके बारे में ठीक से पता नहीं है। आयुष्मान भारत या राशन कार्ड प्रक्रियाओं के बारे में पूछने का प्रयास करें।",
        "मेरे डेटाबेस में अभी वह जानकारी नहीं है। मैं क्या कर सकता हूँ यह देखने के लिए आप 'मदद' मांग सकते हैं!",
        "क्या आप कृपया उसे दोहरा सकते हैं? मैं सरकारी योजनाओं और आपातकालीन सेवाओं में विशेषज्ञ हूं।"
    ]
}

def get_intent(text):
    t = text.lower()
    if any(x in t for x in ["hi", "hello", "hey", "नमस्ते", "हेलो"]): return "greetings"
    if any(x in t for x in ["help", "what can you do", "मदद", "सहायता"]): return "help"
    if any(x in t for x in ["ayushman", "bharat", "pmjay", "आयुष्मान", "भारत"]): return "ayushman"
    if any(x in t for x in ["ration", "food", "card", "राशन"]): return "ration"
    if any(x in t for x in ["emergency", "police", "112", "108", "पुलिस", "आपातकाल"]): return "emergency"
    if any(x in t for x in ["hospital", "doctor", "medical", "अस्पताल", "डॉक्टर"]): return "hospital"
    return "default"

@app.route("/api/query", methods=["POST"])
def handle_query():
    try:
        data = request.json
        user_text = data.get("text", "")
        lang = data.get("language", "en")
        intent = get_intent(user_text)
        
        response_text = KNOWLEDGE[intent][lang] if intent != "default" else random.choice(FALLBACKS[lang])

        logs_collection.insert_one({
            "text": user_text, "response": response_text, "language": lang, "intent": intent, "timestamp": datetime.utcnow()
        })
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": "Error", "details": str(e)}), 500

@app.route("/api/history", methods=["GET"])
def get_history():
    history = list(logs_collection.find().sort("timestamp", -1).limit(50))
    for item in history:
        item["_id"] = str(item["_id"])
        item["time"] = item["timestamp"].strftime("%b %d, %H:%M")
    return jsonify(history)

@app.route("/api/clear", methods=["POST"])
def clear_history():
    logs_collection.delete_many({})
    return jsonify({"status": "success"})

app = app
