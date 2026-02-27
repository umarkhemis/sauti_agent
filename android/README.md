# SautiAgent Android App

A voice-first AI assistant for low-connectivity users in Uganda, built with Kotlin and Jetpack Compose.

## Requirements

- Android Studio Hedgehog (2023.1.1) or later
- JDK 17
- Android SDK API 26+ (minSdk)
- Android SDK API 34 (compileSdk/targetSdk)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/umarkhemis/sauti_agent.git
cd sauti_agent/android
```

### 2. Open in Android Studio
- Open Android Studio
- Select **File > Open** and navigate to the `android/` folder
- Wait for Gradle sync to complete

### 3. Configure Backend URL
The app connects to the Django backend running at `http://10.0.2.2:8000` (Android emulator's localhost). To change this, edit:
```
app/src/main/java/com/sauti/agent/data/api/RetrofitClient.kt
```

### 4. Start the backend
```bash
cd ../backend
# Follow backend setup instructions
```

### 5. Build & Run
- Connect an Android device or start an emulator (API 26+)
- Click **Run ▶** in Android Studio, or use:
```bash
./gradlew assembleDebug
```

## Architecture

This app follows **MVVM + Clean Architecture**:

```
UI Layer (Compose Screens + ViewModels)
    ↓
Domain/Repository Layer
    ↓
Data Layer (Retrofit API + DataStore)
```

### Key Components

- **`SautiApplication`** — Hilt application class
- **`MainActivity`** — Single activity host for Compose
- **`SautiNavGraph`** — Navigation graph for all screens
- **`SautiApiService`** — Retrofit interface for all backend calls
- **`UserRepository`** — User profile & session management with DataStore persistence
- **`SpeechRepository`** — Audio transcription & TTS
- **`SmsRepository`** — SMS compose & read
- **`ContactsRepository`** — Contact search

## Screens

| Screen | Description |
|--------|-------------|
| **Onboarding** | Language, phone number, telecom setup |
| **Home** | Central hub with large mic button and quick actions |
| **Voice** | Full-screen voice interaction with waveform animation |
| **SMS** | Compose (voice dictation) and Read (TTS playback) tabs |
| **Contacts** | Search and browse contacts |
| **Mobile Money** | USSD-based balance check, send money, buy airtime |

## Permissions

The app requests the following permissions:
- `INTERNET` — API communication
- `RECORD_AUDIO` — Voice recording (requested at runtime)
- `READ_CONTACTS` / `WRITE_CONTACTS` — Contact access
- `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE` — Audio file storage (legacy)

## Dependencies

| Library | Purpose |
|---------|---------|
| Jetpack Compose BOM 2024.02.00 | UI framework |
| Material3 | Design system |
| Navigation Compose | Screen navigation |
| Retrofit 2.9.0 | HTTP client |
| OkHttp 4.12.0 | Network layer |
| Hilt 2.50 | Dependency injection |
| DataStore | Local preferences |
| Coroutines 1.7.3 | Async operations |
| Coil 2.5.0 | Image loading |

## Supported Languages

| Code | Language |
|------|----------|
| `lug` | Luganda |
| `ach` | Acholi |
| `nyn` | Runyankole |
| `lso` | Lusoga |
| `lgg` | Lugbara |
| `eng` | English |
