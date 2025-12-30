#!/usr/bin/env python3
"""
Firebase Firestore Seed Script
Populates the 'responses' collection with curated responses for AwaazSetu.

Usage:
    Set FIREBASE_SERVICE_ACCOUNT environment variable, then run:
    python seed_firebase.py
"""

import os
import json
import sys

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("Error: firebase-admin not installed. Install it with: pip install firebase-admin")
    sys.exit(1)

# ---------------- DATASET ----------------

RESPONSES_DATA = [
    # ========== GENERAL SERVICE ==========
    {
        "service": "general",
        "intent": "greeting",
        "language": "en",
        "keywords": ["hi", "hello", "hey", "good morning", "good evening", "namaste"],
        "response": "Hello! Welcome to AwaazSetu. I'm here to help you with government and healthcare services. How can I assist you today?"
    },
    {
        "service": "general",
        "intent": "greeting",
        "language": "hi",
        "keywords": ["नमस्ते", "नमस्कार", "हेलो", "हाय", "सुप्रभात"],
        "response": "नमस्ते! आवाज़सेतु में आपका स्वागत है। मैं सरकारी और स्वास्थ्य सेवाओं में आपकी मदद के लिए यहाँ हूँ। मैं आपकी कैसे सहायता कर सकता हूँ?"
    },
    {
        "service": "general",
        "intent": "help",
        "language": "en",
        "keywords": ["help", "what can you do", "how can you help", "what services"],
        "response": "I can help you with government services like Ayushman Bharat, ration cards, pensions, Aadhar, voter ID, housing schemes, and certificates. I also provide healthcare guidance for common health issues. What would you like to know?"
    },
    {
        "service": "general",
        "intent": "help",
        "language": "hi",
        "keywords": ["मदद", "सहायता", "क्या कर सकते हो", "क्या सेवाएं"],
        "response": "मैं आयुष्मान भारत, राशन कार्ड, पेंशन, आधार, वोटर आईडी, आवास योजनाएं और प्रमाण पत्र जैसी सरकारी सेवाओं में आपकी मदद कर सकता हूँ। मैं सामान्य स्वास्थ्य समस्याओं के लिए मार्गदर्शन भी प्रदान करता हूँ। आप क्या जानना चाहेंगे?"
    },
    {
        "service": "general",
        "intent": "about_platform",
        "language": "en",
        "keywords": ["about", "what is", "tell me about", "explain"],
        "response": "AwaazSetu is your voice bridge to government and healthcare services. You can ask questions in Hindi or English, and I'll provide information about various services and health guidance."
    },
    {
        "service": "general",
        "intent": "about_platform",
        "language": "hi",
        "keywords": ["के बारे में", "क्या है", "बताओ", "समझाओ"],
        "response": "आवाज़सेतु सरकारी और स्वास्थ्य सेवाओं के लिए आपका आवाज़ पुल है। आप हिंदी या अंग्रेजी में सवाल पूछ सकते हैं, और मैं विभिन्न सेवाओं और स्वास्थ्य मार्गदर्शन के बारे में जानकारी प्रदान करूंगा।"
    },
    {
        "service": "general",
        "intent": "default",
        "language": "en",
        "keywords": [],
        "response": "I'm here to help you with government and healthcare services. Could you please tell me more about what you need?"
    },
    {
        "service": "general",
        "intent": "default",
        "language": "hi",
        "keywords": [],
        "response": "मैं सरकारी और स्वास्थ्य सेवाओं में आपकी मदद के लिए यहाँ हूँ। कृपया मुझे बताएं कि आपको क्या चाहिए?"
    },
    {
        "service": "general",
        "intent": "emergency_numbers",
        "language": "en",
        "keywords": ["emergency number", "police number", "ambulance number", "fire number", "help number", "sos"],
        "response": "Here are important emergency numbers in India. Police 112. Ambulance 108. Fire 101. Women helpline 181. Child helpline 1098. Disaster management 1078. Please call these numbers in case of emergency."
    },
    {
        "service": "general",
        "intent": "emergency_numbers",
        "language": "hi",
        "keywords": ["इमरजेंसी नंबर", "पुलिस नंबर", "एम्बुलेंस नंबर", "फायर ब्रिगेड नंबर", "मदद नंबर", "आपातकाल नंबर"],
        "response": "भारत में जरूरी आपातकालीन नंबर हैं। पुलिस 112। एम्बुलेंस 108। फायर ब्रिगेड 101। महिला हेल्पलाइन 181। चाइल्ड हेल्पलाइन 1098। आपदा प्रबंधन 1078। कृपया आपातकाल में इन नंबरों पर कॉल करें।"
    },
    
    # ========== GOVERNMENT SERVICE ==========
    {
        "service": "government",
        "intent": "ayushman_bharat",
        "language": "en",
        "keywords": ["ayushman", "health card", "pmjay"],
        "response": "Ayushman Bharat provides free healthcare coverage up to 5 lakh rupees per family per year at government and empaneled private hospitals. To check eligibility, visit pmjay.gov.in or call 14555. You can also visit your nearest Common Service Center."
    },
    {
        "service": "government",
        "intent": "ayushman_bharat",
        "language": "hi",
        "keywords": ["आयुष्मान", "स्वास्थ्य कार्ड", "पीएमजेएवाई"],
        "response": "आयुष्मान भारत सरकारी और पैनल में शामिल निजी अस्पतालों में प्रति परिवार प्रति वर्ष 5 लाख रुपये तक मुफ्त स्वास्थ्य कवरेज प्रदान करता है। पात्रता जांचने के लिए, pmjay.gov.in पर जाएं या 14555 पर कॉल करें। आप अपने निकटतम कॉमन सर्विस सेंटर भी जा सकते हैं।"
    },
    {
        "service": "government",
        "intent": "ration_card",
        "language": "en",
        "keywords": ["ration card", "ration", "food card"],
        "response": "To apply for a ration card, visit your nearest ration office or Common Service Center. You'll need proof of identity, address proof, and a passport-size photo. The process is usually free and takes 15-30 days. You can also apply online through your state's food and civil supplies department website."
    },
    {
        "service": "government",
        "intent": "ration_card",
        "language": "hi",
        "keywords": ["राशन कार्ड", "राशन"],
        "response": "राशन कार्ड के लिए आवेदन करने के लिए, अपने निकटतम राशन कार्यालय या कॉमन सर्विस सेंटर जाएं। आपको पहचान प्रमाण, पता प्रमाण और पासपोर्ट साइज फोटो की आवश्यकता होगी। प्रक्रिया आमतौर पर मुफ्त है और 15-30 दिन लगते हैं। आप अपने राज्य के खाद्य और नागरिक आपूर्ति विभाग की वेबसाइट के माध्यम से ऑनलाइन भी आवेदन कर सकते हैं।"
    },
    {
        "service": "government",
        "intent": "pension",
        "language": "en",
        "keywords": ["pension", "old age pension", "widow pension"],
        "response": "For pension schemes, visit your district social welfare office or Common Service Center. Old age pension is available for people above 60 years. You'll need age proof, income certificate, and bank account details. The monthly pension amount varies by state, typically 500 to 2000 rupees."
    },
    {
        "service": "government",
        "intent": "pension",
        "language": "hi",
        "keywords": ["पेंशन", "वृद्धावस्था पेंशन", "विधवा पेंशन"],
        "response": "पेंशन योजनाओं के लिए, अपने जिला सामाजिक कल्याण कार्यालय या कॉमन सर्विस सेंटर जाएं। 60 वर्ष से अधिक उम्र के लोगों के लिए वृद्धावस्था पेंशन उपलब्ध है। आपको आयु प्रमाण, आय प्रमाण पत्र और बैंक खाता विवरण की आवश्यकता होगी। मासिक पेंशन राशि राज्य के अनुसार अलग-अलग होती है, आमतौर पर 500 से 2000 रुपये।"
    },
    {
        "service": "government",
        "intent": "aadhar",
        "language": "en",
        "keywords": ["aadhar", "aadhaar", "uid", "unique id"],
        "response": "To apply for Aadhar, visit any Aadhar enrollment center with proof of identity, address, and date of birth. The enrollment is free. You can find nearby centers at uidai.gov.in or call 1947. For updates or corrections, visit the same website or your nearest enrollment center."
    },
    {
        "service": "government",
        "intent": "aadhar",
        "language": "hi",
        "keywords": ["आधार", "यूआईडी"],
        "response": "आधार के लिए आवेदन करने के लिए, पहचान प्रमाण, पता और जन्म तिथि के साथ किसी भी आधार नामांकन केंद्र पर जाएं। नामांकन मुफ्त है। आप uidai.gov.in पर या 1947 पर कॉल करके निकटतम केंद्र पा सकते हैं। अपडेट या सुधार के लिए, उसी वेबसाइट या अपने निकटतम नामांकन केंद्र पर जाएं।"
    },
    {
        "service": "government",
        "intent": "voter_id",
        "language": "en",
        "keywords": ["voter", "voting", "voter id", "election card"],
        "response": "To apply for a voter ID card, visit your nearest electoral registration office or apply online at nvsp.in. You'll need proof of age and address. The process is free. You can also check your voter status and download your card from the same website."
    },
    {
        "service": "government",
        "intent": "voter_id",
        "language": "hi",
        "keywords": ["वोटर", "मतदाता", "वोटर आईडी", "चुनाव कार्ड"],
        "response": "वोटर आईडी कार्ड के लिए आवेदन करने के लिए, अपने निकटतम निर्वाचन पंजीकरण कार्यालय जाएं या nvsp.in पर ऑनलाइन आवेदन करें। आपको आयु और पते का प्रमाण चाहिए। प्रक्रिया मुफ्त है। आप उसी वेबसाइट से अपनी वोटर स्थिति भी जांच सकते हैं और अपना कार्ड डाउनलोड कर सकते हैं।"
    },
    {
        "service": "government",
        "intent": "housing",
        "language": "en",
        "keywords": ["housing", "house", "home", "pm awas", "housing scheme"],
        "response": "For housing schemes like Pradhan Mantri Awas Yojana, visit your district housing office or apply online at pmaymis.gov.in. Eligibility depends on income and family size. You'll need income certificate, identity proof, and family details. The scheme provides financial assistance for building or buying a house."
    },
    {
        "service": "government",
        "intent": "housing",
        "language": "hi",
        "keywords": ["आवास", "घर", "पीएम आवास", "आवास योजना"],
        "response": "प्रधानमंत्री आवास योजना जैसी आवास योजनाओं के लिए, अपने जिला आवास कार्यालय जाएं या pmaymis.gov.in पर ऑनलाइन आवेदन करें। पात्रता आय और परिवार के आकार पर निर्भर करती है। आपको आय प्रमाण पत्र, पहचान प्रमाण और परिवार का विवरण चाहिए। योजना घर बनाने या खरीदने के लिए वित्तीय सहायता प्रदान करती है।"
    },
    {
        "service": "government",
        "intent": "birth_certificate",
        "language": "en",
        "keywords": ["birth certificate", "birth", "birth registration"],
        "response": "To get a birth certificate, visit your municipal corporation office or Common Service Center. You'll need hospital discharge slip or proof from the hospital where the child was born. The certificate is usually issued within 7-15 days. You can also apply online through your state's birth registration portal."
    },
    {
        "service": "government",
        "intent": "birth_certificate",
        "language": "hi",
        "keywords": ["जन्म प्रमाण पत्र", "जन्म"],
        "response": "जन्म प्रमाण पत्र प्राप्त करने के लिए, अपने नगर निगम कार्यालय या कॉमन सर्विस सेंटर जाएं। आपको अस्पताल से डिस्चार्ज स्लिप या उस अस्पताल से प्रमाण चाहिए जहाँ बच्चे का जन्म हुआ था। प्रमाण पत्र आमतौर पर 7-15 दिनों के भीतर जारी किया जाता है। आप अपने राज्य के जन्म पंजीकरण पोर्टल के माध्यम से ऑनलाइन भी आवेदन कर सकते हैं।"
    },
    {
        "service": "government",
        "intent": "income_certificate",
        "language": "en",
        "keywords": ["income certificate", "income", "income proof"],
        "response": "To get an income certificate, visit your tehsil or district revenue office. You'll need identity proof, address proof, and income details. The certificate is usually issued within 7-10 days. This certificate is needed for various government schemes and benefits."
    },
    {
        "service": "government",
        "intent": "income_certificate",
        "language": "hi",
        "keywords": ["आय प्रमाण पत्र", "आय"],
        "response": "आय प्रमाण पत्र प्राप्त करने के लिए, अपने तहसील या जिला राजस्व कार्यालय जाएं। आपको पहचान प्रमाण, पता प्रमाण और आय विवरण चाहिए। प्रमाण पत्र आमतौर पर 7-10 दिनों के भीतर जारी किया जाता है। यह प्रमाण पत्र विभिन्न सरकारी योजनाओं और लाभों के लिए आवश्यक है।"
    },
    {
        "service": "government",
        "intent": "default",
        "language": "en",
        "keywords": [],
        "response": "For government services, please visit your nearest government office or Common Service Center. You can also call the helpline or visit the official website of the concerned department for more information."
    },
    {
        "service": "government",
        "intent": "default",
        "language": "hi",
        "keywords": [],
        "response": "सरकारी सेवाओं के लिए, कृपया अपने निकटतम सरकारी कार्यालय या कॉमन सर्विस सेंटर जाएं। अधिक जानकारी के लिए आप हेल्पलाइन पर कॉल कर सकते हैं या संबंधित विभाग की आधिकारिक वेबसाइट पर जा सकते हैं।"
    },
    
    # ========== HEALTHCARE SERVICE ==========
    {
        "service": "healthcare",
        "intent": "fever",
        "language": "en",
        "keywords": ["fever", "temperature", "hot"],
        "response": "If you have fever, rest well, drink plenty of fluids, and take paracetamol as directed. If fever persists for more than 3 days, is very high above 103 degrees, or you have other symptoms like severe headache or difficulty breathing, please visit a government hospital or contact a healthcare provider immediately."
    },
    {
        "service": "healthcare",
        "intent": "fever",
        "language": "hi",
        "keywords": ["बुखार", "तापमान"],
        "response": "अगर बुखार है, तो अच्छी तरह आराम करें, खूब पानी पिएं, और निर्देशानुसार पैरासिटामोल लें। अगर बुखार 3 दिन से ज्यादा रहता है, 103 डिग्री से ऊपर बहुत ज्यादा है, या आपको गंभीर सिरदर्द या सांस लेने में तकलीफ जैसे अन्य लक्षण हैं, तो कृपया तुरंत सरकारी अस्पताल जाएं या स्वास्थ्य सेवा प्रदाता से संपर्क करें।"
    },
    {
        "service": "healthcare",
        "intent": "cough_cold",
        "language": "en",
        "keywords": ["cough", "cold", "sneezing", "runny nose"],
        "response": "For cough and cold, rest well, drink warm fluids like tea or soup, and use steam inhalation. If symptoms persist for more than a week, worsen, or you have difficulty breathing, please visit a government hospital or primary health center for proper evaluation."
    },
    {
        "service": "healthcare",
        "intent": "cough_cold",
        "language": "hi",
        "keywords": ["खांसी", "जुकाम", "सर्दी", "नाक बहना"],
        "response": "खांसी और जुकाम के लिए, अच्छी तरह आराम करें, चाय या सूप जैसे गर्म तरल पदार्थ पिएं, और भाप लें। अगर लक्षण एक सप्ताह से अधिक समय तक बने रहते हैं, बिगड़ते हैं, या आपको सांस लेने में कठिनाई होती है, तो कृपया उचित मूल्यांकन के लिए सरकारी अस्पताल या प्राथमिक स्वास्थ्य केंद्र जाएं।"
    },
    {
        "service": "healthcare",
        "intent": "stomach_pain",
        "language": "en",
        "keywords": ["stomach", "stomach pain", "abdominal pain", "belly pain"],
        "response": "For stomach pain, avoid spicy and oily foods, drink plenty of water, and rest. If the pain is severe, persistent for more than 2 days, or accompanied by vomiting, fever, or blood in stool, please visit a government hospital or healthcare center immediately for proper evaluation."
    },
    {
        "service": "healthcare",
        "intent": "stomach_pain",
        "language": "hi",
        "keywords": ["पेट", "पेट दर्द", "उदर दर्द"],
        "response": "पेट दर्द के लिए, मसालेदार और तैलीय भोजन से बचें, खूब पानी पिएं, और आराम करें। अगर दर्द गंभीर है, 2 दिन से अधिक समय तक बना रहता है, या उल्टी, बुखार, या मल में खून के साथ है, तो कृपया उचित मूल्यांकन के लिए तुरंत सरकारी अस्पताल या स्वास्थ्य केंद्र जाएं।"
    },
    {
        "service": "healthcare",
        "intent": "headache",
        "language": "en",
        "keywords": ["headache", "head pain", "migraine"],
        "response": "For headache, rest in a quiet, dark room, drink water, and you may take paracetamol as directed. If headaches are frequent, very severe, or accompanied by vision problems, fever, or neck stiffness, please visit a government hospital or healthcare provider for proper evaluation."
    },
    {
        "service": "healthcare",
        "intent": "headache",
        "language": "hi",
        "keywords": ["सिर दर्द", "माइग्रेन", "सिर में दर्द"],
        "response": "सिरदर्द के लिए, शांत, अंधेरे कमरे में आराम करें, पानी पिएं, और आप निर्देशानुसार पैरासिटामोल ले सकते हैं। अगर सिरदर्द बार-बार होते हैं, बहुत गंभीर हैं, या दृष्टि समस्याओं, बुखार, या गर्दन में अकड़न के साथ हैं, तो कृपया उचित मूल्यांकन के लिए सरकारी अस्पताल या स्वास्थ्य सेवा प्रदाता से संपर्क करें।"
    },
    {
        "service": "healthcare",
        "intent": "pregnancy",
        "language": "en",
        "keywords": ["pregnancy", "pregnant", "baby", "maternal"],
        "response": "For pregnancy-related care, register at your nearest government hospital or primary health center for antenatal checkups. Regular checkups are important for the health of both mother and baby. You can also avail benefits under government schemes like Pradhan Mantri Matru Vandana Yojana. For any concerns, consult a healthcare provider."
    },
    {
        "service": "healthcare",
        "intent": "pregnancy",
        "language": "hi",
        "keywords": ["गर्भावस्था", "गर्भवती", "बच्चा", "मातृ"],
        "response": "गर्भावस्था संबंधी देखभाल के लिए, प्रसवपूर्व जांच के लिए अपने निकटतम सरकारी अस्पताल या प्राथमिक स्वास्थ्य केंद्र में पंजीकरण कराएं। नियमित जांच माँ और बच्चे दोनों के स्वास्थ्य के लिए महत्वपूर्ण है। आप प्रधानमंत्री मातृ वंदना योजना जैसी सरकारी योजनाओं के तहत लाभ भी प्राप्त कर सकते हैं। किसी भी चिंता के लिए, स्वास्थ्य सेवा प्रदाता से परामर्श करें।"
    },
    {
        "service": "healthcare",
        "intent": "vaccination",
        "language": "en",
        "keywords": ["vaccination", "vaccine", "immunization", "injection"],
        "response": "Vaccination is available free of cost at government hospitals and primary health centers. Children should receive all recommended vaccines as per the immunization schedule. Adults can also get vaccines for diseases like COVID-19, tetanus, and others. Visit your nearest government health center for vaccination schedules and availability."
    },
    {
        "service": "healthcare",
        "intent": "vaccination",
        "language": "hi",
        "keywords": ["टीका", "वैक्सीन", "टीकाकरण", "इंजेक्शन"],
        "response": "सरकारी अस्पतालों और प्राथमिक स्वास्थ्य केंद्रों में टीकाकरण मुफ्त में उपलब्ध है। बच्चों को टीकाकरण कार्यक्रम के अनुसार सभी अनुशंसित टीके मिलने चाहिए। वयस्क भी COVID-19, टेटनस और अन्य बीमारियों के लिए टीके प्राप्त कर सकते हैं। टीकाकरण कार्यक्रम और उपलब्धता के लिए अपने निकटतम सरकारी स्वास्थ्य केंद्र पर जाएं।"
    },
    {
        "service": "healthcare",
        "intent": "child_health",
        "language": "en",
        "keywords": ["child", "baby", "infant", "kids", "children"],
        "response": "For child health, ensure regular checkups at government health centers, complete all vaccinations, and maintain proper nutrition. If your child has persistent symptoms, high fever, difficulty breathing, or is not eating or drinking, please visit a government hospital or pediatrician immediately."
    },
    {
        "service": "healthcare",
        "intent": "child_health",
        "language": "hi",
        "keywords": ["बच्चा", "शिशु", "बाल", "बच्चे"],
        "response": "बच्चे के स्वास्थ्य के लिए, सरकारी स्वास्थ्य केंद्रों पर नियमित जांच सुनिश्चित करें, सभी टीकाकरण पूरे करें, और उचित पोषण बनाए रखें। अगर आपके बच्चे में लगातार लक्षण हैं, तेज बुखार है, सांस लेने में कठिनाई है, या खाना-पीना नहीं है, तो कृपया तुरंत सरकारी अस्पताल या बाल रोग विशेषज्ञ से संपर्क करें।"
    },
    {
        "service": "healthcare",
        "intent": "emergency_guidance",
        "language": "en",
        "keywords": ["emergency", "urgent", "immediate", "critical"],
        "response": "For medical emergencies, call 108 for ambulance service or go to the nearest government hospital immediately. Signs of emergency include severe chest pain, difficulty breathing, loss of consciousness, severe injury, or uncontrolled bleeding. Do not delay seeking medical help in emergencies."
    },
    {
        "service": "healthcare",
        "intent": "emergency_guidance",
        "language": "hi",
        "keywords": ["आपातकाल", "जरूरी", "तुरंत", "गंभीर"],
        "response": "चिकित्सा आपातकाल के लिए, एम्बुलेंस सेवा के लिए 108 पर कॉल करें या तुरंत निकटतम सरकारी अस्पताल जाएं। आपातकाल के संकेतों में गंभीर सीने में दर्द, सांस लेने में कठिनाई, बेहोशी, गंभीर चोट, या अनियंत्रित रक्तस्राव शामिल हैं। आपातकाल में चिकित्सा सहायता लेने में देरी न करें।"
    },
    {
        "service": "healthcare",
        "intent": "default",
        "language": "en",
        "keywords": [],
        "response": "For healthcare concerns, please visit a government hospital or primary health center. For emergencies, call 108. If you have specific symptoms, it's best to consult a healthcare provider for proper evaluation and guidance."
    },
    {
        "service": "healthcare",
        "intent": "default",
        "language": "hi",
        "keywords": [],
        "response": "स्वास्थ्य संबंधी चिंताओं के लिए, कृपया सरकारी अस्पताल या प्राथमिक स्वास्थ्य केंद्र जाएं। आपातकाल के लिए, 108 पर कॉल करें। अगर आपके पास विशिष्ट लक्षण हैं, तो उचित मूल्यांकन और मार्गदर्शन के लिए स्वास्थ्य सेवा प्रदाता से परामर्श करना सबसे अच्छा है।"
    },
]

# ---------------- SEED FUNCTION ----------------

def seed_firebase():
    """Seed Firestore with response data."""
    
    # Initialize Firebase
    firebase_service_account = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
    
    if not firebase_service_account:
        print("Error: FIREBASE_SERVICE_ACCOUNT environment variable not set.")
        print("Please set it with your Firebase service account JSON as a string.")
        sys.exit(1)
    
    try:
        service_account_info = json.loads(firebase_service_account)
    except json.JSONDecodeError:
        print("Error: FIREBASE_SERVICE_ACCOUNT is not valid JSON.")
        sys.exit(1)
    
    try:
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing responses...")
        responses_ref = db.collection("responses")
        docs = responses_ref.stream()
        for doc in docs:
            doc.reference.delete()
        
        # Add all responses
        print(f"Adding {len(RESPONSES_DATA)} responses to Firestore...")
        batch = db.batch()
        batch_size = 0
        total_added = 0
        
        for response_data in RESPONSES_DATA:
            doc_ref = db.collection("responses").document()
            batch.set(doc_ref, response_data)
            batch_size += 1
            total_added += 1
            
            # Firestore batch limit is 500
            if batch_size >= 500:
                batch.commit()
                print(f"Committed batch of {batch_size} documents...")
                batch = db.batch()
                batch_size = 0
        
        # Commit remaining documents
        if batch_size > 0:
            batch.commit()
            print(f"Committed final batch of {batch_size} documents...")
        
        print(f"\n✅ Successfully seeded {total_added} responses to Firestore!")
        print(f"Collection: 'responses'")
        print(f"Total documents: {total_added}")
        
    except Exception as e:
        print(f"Error seeding Firebase: {e}")
        sys.exit(1)

if __name__ == "__main__":
    seed_firebase()

