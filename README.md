# 🎙️ AwaazSetu & Sarthi  
### 🌏 *Bridging the Digital Divide for Bharat via Voice & Offline Access*

**AwaazSetu** (Web) and **Sarthi** (Android APK) are voice-first digital assistants designed to make **government services, healthcare guidance, and emergency information** accessible to everyone—regardless of literacy level or internet connectivity.

---

## 📱 Introducing: Sarthi (Android APK)
**Sarthi** is the native evolution of AwaazSetu, built specifically for the realities of rural India: **low bandwidth and zero-connectivity zones.**

### 🌟 Key Android Features (Offline-First)
- **True Offline Functionality:** Unlike the web version, the Sarthi APK allows users to access the core database of emergency numbers and health guidance without any internet connection.
- **Intelligent Sync:** Designed for "momentary connectivity." The app queues data and updates itself the second a signal is restored.
- **Low-Bandwidth Optimization:** Engineered to run smoothly on budget Android devices and 2G networks.
- **Voice-First UI:** Optimized for high-performance speech recognition on mobile hardware.

---

## 💻 AwaazSetu (Web Platform)
The web-based gateway for instant access via browser.

🚨 **IMPORTANT:** Voice features work best in **Google Chrome**. Please allow microphone access when prompted.

🔗 **LIVE DEMO:** [https://awaaz-setu-2.onrender.com/](https://awaaz-setu-2.onrender.com/)

---

## 🎙️ Supported Voice & Text Commands
Both platforms use a **keyword-based intent system** to ensure 100% accuracy and safety.

### 🔹 Emergency & Safety
* **Commands:** "Call Police", "Ambulance number", "Emergency numbers in India", "Women helpline".
* **Output:** Instant access to verified numbers like **112, 108, 101, 1098**.

### 🔹 Government Schemes & Documents
* **Commands:** "Ayushman Bharat", "PM Awas Yojana", "Ration card kaise banaye", "Aadhaar update", "Voter ID apply".
* **Focus:** Simplifying complex portals into simple spoken instructions.

### 🔹 Healthcare & Pregnancy
* **Commands:** "I have fever", "Pregnancy care", "Government pregnancy scheme", "Stomach pain", "Free treatment scheme".

### 🔹 Pension & Senior Citizens
* **Commands:** "Old age pension", "Pension scheme", "Senior citizen help".

---

## 💡 Why Sarthi & AwaazSetu?

In rural India, millions face **The Connectivity Gap**:
- ❌ **Low Digital Literacy:** Navigating complex UIs is difficult.
- ❌ **Language Barriers:** Most portals are English-heavy.
- ❌ **Unstable Internet:** Web apps fail when the signal drops.

**Our Solution:**
1.  **Natural Interaction:** Speaking is easier than typing.
2.  **Language Inclusion:** Supports Hindi and English (Hinglish).
3.  **Resilience:** Sarthi (APK) stays functional when the internet vanishes.
4.  **No Hallucinations:** Rule-based responses ensure users get verified, safe information every time.

---

## 🧭 How It Works

1.  **User Speaks:** Tap the mic and ask a question (e.g., "राशन कार्ड कैसे बनवाएं?").
2.  **Intent Detection:** The system analyzes the query using local (APK) or cloud (Web) keyword mapping.
3.  **Knowledge Retrieval:** Sarthi fetches verified data from its **Offline SQLite/Firebase** cache.
4.  **Voice Response:** The answer is displayed visually **and read aloud** via Text-to-Speech.

---

## 🛠️ Tech Stack

### **Mobile (Sarthi APK)**
- **Java/Kotlin & XML:** Native Android development.
- **SQLite / Room:** For robust offline data storage.
- **WorkManager:** For background synchronization when internet returns.

### **Web (AwaazSetu)**
- **Python Flask:** Backend API.
- **Web Speech API:** For browser-based voice-to-text.
- **Firebase Firestore:** Multilingual database.

---

## 🚀 Installation & Setup

### **For Android (Sarthi)**
1. Download the `Sarthi.apk` from the [Releases](#) section.
2. Enable "Install from Unknown Sources" in settings.
3. Open and start speaking—even without Wi-Fi!

### **For Web (Local Development)**
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
