## 🎙️ SautiAgent — Initial Project Setup

This PR sets up the complete project structure for SautiAgent, a multilingual voice AI assistant for elderly and low-literacy users in Uganda.

### What's included

#### 📁 Root
- `README.md` — Full project documentation with problem statement, solution, tech stack, and setup instructions
- `.gitignore` — Covers Python/Django, Android/Kotlin, environment files, IDE files
- `docker-compose.yml` — Backend + PostgreSQL + Redis + Celery

#### 🐍 Backend (Django + DRF)
- `backend/manage.py`
- `backend/requirements.txt` — All dependencies
- `backend/.env.example` — All environment variables documented
- `backend/Dockerfile`
- `backend/sautiagent/settings/` — base, development, production settings
- `backend/sautiagent/urls.py` — All API routes wired up
- `backend/apps/users/` — User model with language preference + telecom
- `backend/apps/speech/sunbird_client.py` — Full Sunbird AI client (STT, TTS, Translation, Language Detection)
- `backend/apps/intent/intent_engine.py` — GPT-4o intent classification engine
- `backend/apps/dialogue/dialogue_manager.py` — Confirmation flows, error recovery, filler messages in all 6 languages
- `backend/apps/ussd/ussd_codes.py` — Complete MTN + Airtel Uganda USSD codes
- `backend/apps/ussd/response_parser.py` — USSD response parser with spoken output

#### 📱 Android (Kotlin)
- `android/app/src/main/java/com/sautiagent/onboarding/LanguageOnboardingActivity.kt` — Multilingual welcome loop + passive language detection
- `android/app/src/main/java/com/sautiagent/voice/MainVoiceActivity.kt` — Single mic button UI, volume-down-twice trigger
- `android/app/src/main/java/com/sautiagent/ussd/USSDHandler.kt` — TelephonyManager USSD execution
- `android/app/src/main/java/com/sautiagent/ussd/USSDCodes.kt` — All Uganda USSD codes on-device
- `android/app/src/main/java/com/sautiagent/utils/SessionManager.kt` — Language + session persistence

#### 📚 Docs
- `docs/architecture.md` — Full system architecture with diagrams
- `docs/setup_guide.md` — Developer setup for backend and Android
- `assets/audio/welcome/README.md` — Instructions for generating welcome audio files

### Key Design Decisions
- **Android only for MVP** — No IVR, no feature phone support in v1
- **One button UI** — Single mic button, no menus, no text to read
- **Sunbird AI** — Luganda, Acholi, Runyankole, Lusoga, Lugbara, English
- **Passive language detection** — User speaks, system detects language automatically
- **PIN security** — SautiAgent never captures PINs, uses STK Push
- **All responses spoken** — Nothing critical is text-only