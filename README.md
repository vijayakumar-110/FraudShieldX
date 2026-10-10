# FraudShield X

Hackathon-ready starter: Android SMS detector + FastAPI fraud engine + React dashboard.

## Run backend
cd backend
python -m venv venv
# Windows: venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload

## Run dashboard
cd dashboard
npm install
npm run dev

## Android
Open `android/` in Android Studio, sync Gradle, and run. The app requests SMS permissions and sends incoming SMS text to the backend. Set the backend URL in `NetworkConfig.kt`.

Important: the app does not bypass WhatsApp privacy/security. WhatsApp/email require user-authorized or official integrations.
