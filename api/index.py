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
        "en": "Hello! I am AwaazSetu, your government service assistant. I can provide information on health schemes, ration cards, and emergency aid. How can I help you?",
        "hi": "नमस्ते! मैं आवाज़सेतु हूँ, आपका सरकारी सेवा सहायक। मैं स्वास्थ्य योजनाओं, राशन कार्ड और आपातकालीन सहायता के बारे में जानकारी दे सकता हूँ।"
    },
    "help": {
        "en": "I can help you with: 1. Ayushman Bharat (Health), 2. Ration Card application, 3. PM Kisan status, 4. Emergency Numbers, or 5. Government Hospitals.",
        "hi": "मैं आपकी मदद कर सकता हूँ: 1. आयुष्मान भारत, 2. राशन कार्ड आवेदन, 3. पीएम किसान स्थिति, 4. आपातकालीन नंबर, या 5. सरकारी अस्पताल।"
    },
    "ayushman": {
        "en": "Ayushman Bharat (PM-JAY) provides ₹5 Lakhs free health insurance per family per year. Apply at any PMJAY hospital with your Aadhaar and Ration Card.",
        "hi": "आयुष्मान भारत (PM-JAY) प्रति परिवार प्रति वर्ष ₹5 लाख का मुफ्त स्वास्थ्य बीमा प्रदान करता है। आधार और राशन कार्ड के साथ किसी भी PMJAY अस्पताल में आवेदन करें।"
    },
    "ration": {
        "en": "For a Ration Card, visit your State's Food portal or local office. You need identity proof, address proof, and an Income Certificate. Processing takes 15-30 days.",
        "hi": "राशन कार्ड के लिए, अपने राज्य के खाद्य पोर्टल या स्थानीय कार्यालय पर जाएं। आपको पहचान प्रमाण, पता प्रमाण और आय प्रमाण पत्र की आवश्यकता होगी।"
    },
    "emergency": {
        "en": "Emergency numbers: Dial 112 for All-in-one assistance, 100 for Police, 108 for Ambulance, and 101 for Fire services. Help is available 24/7.",
        "hi": "आपातकालीन नंबर: सभी के लिए 112, पुलिस के लिए 100, एम्बुलेंस के लिए 108 और अग्निशमन के लिए 101 डायल करें। सहायता 24/7 उपलब्ध है।"
    }
}

FALLBACKS = {
    "en": ["I'm not sure about that. Try asking about Ayushman Bharat or Ration Card processes.", "I am still learning! Try asking for 'Help' to see what I can do."],
    "hi": ["मुझे इसके बारे में ठीक से पता नहीं है। आयुष्मान भारत या राशन कार्ड के बारे में पूछने का प्रयास करें।", "मैं अभी सीख रहा हूँ! सेवाओं के लिए 'मदद' मांगें।"]
}

def get_intent(text):
    t = text.lower()
    if any(x in t for x in ["hi", "hello", "नमस्ते", "हेलो"]): return "greetings"
    if any(x in t for x in ["help", "मदद", "सहायता"]): return "help"
    if any(x in t for x in ["ayushman", "bharat", "आयुष्मान"]): return "ayushman"
    if any(x in t for x in ["ration", "राशन"]): return "ration"
    if any(x in t for x in ["emergency", "police", "आपातकाल"]): return "emergency"
    return "default"

@app.route("/api/query", methods=["POST"])
def handle_query():
    try:
        data = request.json
        user_text = data.get("text", "")
        lang = data.get("language", "en")
        intent = get_intent(user_text)
        response_text = KNOWLEDGE[intent][lang] if intent != "default" else random.choice(FALLBACKS[lang])
        logs_collection.insert_one({"text": user_text, "response": response_text, "language": lang, "timestamp": datetime.utcnow()})
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
