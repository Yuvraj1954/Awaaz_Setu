# AwaazSetu - Voice Bridge to Services

## Overview
AwaazSetu is a voice-first platform designed to help rural users access government and healthcare information. It provides information in both English and Hindi about essential services like ration cards, pensions, birth certificates, voter ID, Aadhaar, and basic healthcare guidance.

## Architecture
- **Backend**: Python Flask server (app.py)
- **Frontend**: Static HTML/CSS/JavaScript served by Flask
- **Port**: 5000 (0.0.0.0)

## Project Structure
```
/
├── app.py              # Flask backend with API routes
├── public/             # Static frontend files
│   ├── index.html      # Main HTML page
│   ├── styles.css      # Styling
│   └── app.js          # Frontend JavaScript
├── requirements.txt    # Python dependencies
└── package.json        # NPM scripts (for running Flask)
```

## Running the Application
The application runs via the "Start application" workflow which executes `python app.py`.

## API Endpoints
- `GET /` - Serves the main HTML page
- `POST /api/query` - Processes user queries
  - Body: `{ "text": "query", "service": "government|healthcare", "language": "en|hi" }`
  - Returns: Response with relevant information

## Dependencies
- Flask 3.0.0
- flask-cors 4.0.0
