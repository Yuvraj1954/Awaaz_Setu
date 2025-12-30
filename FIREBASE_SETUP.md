# Firebase Setup Guide

## Quick Setup

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project or use existing one
   - Enable Firestore Database (start in production mode)

2. **Get Service Account Key**
   - Go to Project Settings → Service Accounts
   - Click "Generate new private key"
   - Download the JSON file

3. **Set Environment Variable**
   
   **For local development:**
   ```bash
   export FIREBASE_SERVICE_ACCOUNT='{"type":"service_account","project_id":"your-project",...}'
   ```
   
   **For Render/Production:**
   - Go to your Render dashboard
   - Add environment variable: `FIREBASE_SERVICE_ACCOUNT`
   - Paste the entire JSON content as the value

4. **Seed the Database**
   ```bash
   python seed_firebase.py
   ```
   
   This will populate Firestore with all curated responses for:
   - General service (greetings, help, about)
   - Government service (8 intents)
   - Healthcare service (8 intents)
   - Both English and Hindi languages

## Database Structure

**Collection:** `responses`

**Document Fields:**
- `service`: "general" | "government" | "healthcare"
- `intent`: Intent identifier (e.g., "greeting", "ayushman_bharat", "fever")
- `language`: "en" | "hi"
- `keywords`: Array of keywords for matching
- `response`: The actual response text (spoken-style)

## Intent Coverage

### General Service
- `greeting` - Hi, hello, namaste responses
- `help` - What can you do?
- `about_platform` - About AwaazSetu
- `default` - Fallback response

### Government Service
- `ayushman_bharat` - Health card information
- `ration_card` - Ration card application
- `pension` - Pension schemes
- `aadhar` - Aadhar card services
- `voter_id` - Voter ID card
- `housing` - Housing schemes (PMAY)
- `birth_certificate` - Birth certificate
- `income_certificate` - Income certificate
- `default` - Fallback response

### Healthcare Service
- `fever` - Fever guidance
- `cough_cold` - Cough and cold
- `stomach_pain` - Stomach pain
- `headache` - Headache guidance
- `pregnancy` - Pregnancy care
- `vaccination` - Vaccination information
- `child_health` - Child health guidance
- `emergency_guidance` - Emergency situations
- `default` - Fallback response

## Fallback Behavior

If Firebase is not configured or unavailable:
- The app uses safe fallback responses
- Never crashes - always returns a response
- Greeting detection still works
- All features remain functional

## Testing

1. **Test Greeting:**
   - Say "Hi" or "नमस्ते"
   - Should respond with greeting message

2. **Test Government Service:**
   - Select "Government Services"
   - Ask about "Ayushman Bharat" or "राशन कार्ड"
   - Should return relevant information

3. **Test Healthcare Service:**
   - Select "Healthcare"
   - Ask about "fever" or "बुखार"
   - Should return health guidance

4. **Test Fallback:**
   - Ask something not in the database
   - Should return appropriate default response

