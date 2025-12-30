# AwaazSetu - Voice Bridge Platform

A voice-first, low-bandwidth, multilingual platform for rural and non-tech users to access government and healthcare information.

## Features

- **Bilingual Support**: Hindi and English
- **Two Service Categories**:
  - Government Services (Ration Card, Pension, Birth Certificate, Voter ID, Aadhaar)
  - Healthcare (Fever, Cold & Cough, Stomach Pain, Vaccination, Pregnancy Care)
- **Mobile-First Design**: Optimized for small screens and touch interfaces
- **Low-Bandwidth**: Minimal CSS, no heavy frameworks
- **Conversational Responses**: Simple, safe, and easy-to-understand answers

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Flask (Python)
- **No heavy frameworks or libraries**

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Select your preferred language (English or Hindi)
2. Choose a service category (Government Services or Healthcare)
3. Tap the microphone button
4. Type your question in the text field (simulating voice input)
5. Submit your query
6. Receive a simple, conversational response

## Project Structure

```
AwaazSetu/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── public/
│   ├── index.html        # Main HTML file
│   ├── styles.css        # Minimal CSS styling
│   └── app.js            # Frontend JavaScript
└── README.md             # This file
```

## Design Principles

- Large, touchable buttons for ease of use
- Clear visual feedback
- Minimal data transfer
- Simple, conversational language
- Mobile-first responsive design
- High contrast for readability

## Example Queries

**Government Services (English)**:
- "How do I get a ration card?"
- "Tell me about old age pension"
- "I need a voter ID"

**Healthcare (Hindi)**:
- "बुखार है क्या करूं?"
- "बच्चे का टीकाकरण कैसे कराएं?"
- "पेट में दर्द है"

## Safety & Privacy

- No user data is stored
- All responses are pre-vetted and safe
- No external API calls
- Works offline after initial load
