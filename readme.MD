Music Assistant Alexa Skill (Docker-based, Native Playback)

This project provides a self-hosted Alexa Skill that integrates directly with Music Assistant using native Alexa AudioPlayer APIs.

It is designed as a modern replacement for AlexaPy-based solutions and focuses on low latency, correct playback state handling, and clean architecture.

✨ Features

🎵 Native Music Assistant queue integration

⚡ Instant pause / resume (no AlexaPy delays)

🐳 Fully Docker & Docker Compose based

🧠 Alexa acts as pure audio output, MA remains the playback authority

🔁 Proper playback offset synchronization

🔐 Ready for HTTPS reverse proxies (Caddy / Traefik / Cloudflare Tunnel)

🧱 Architecture Overview
Alexa Device
     │
     ▼
Alexa Skill (HTTP / AudioPlayer)
     │
     ▼
Music Assistant Alexa API Bridge
     │
     ▼
Music Assistant Core (Queue & Playback)

Components
Component	Description
Alexa Skill Service	Lambda-compatible HTTP service handling Alexa requests
MA Alexa API	Bridge translating Alexa playback events to Music Assistant
Music Assistant	Owns queues, tracks, playback state
📁 Repository Structure
music-assistant-alexa-skill-prototype/
├── docker-compose.yml
├── .env
│
├── alexa-skill/
│   ├── Dockerfile
│   ├── lambda_function.py
│   ├── music_assistant.py
│   └── requirements.txt
│
├── music-assistant-api/
│   ├── Dockerfile
│   ├── api.py
│   ├── ma_client.py
│   ├── stream.py
│   ├── state.py
│   ├── alexa_state.py
│   └── requirements.txt
│
└── interactionModels/
    └── custom/
        └── de-DE.json

🔧 Prerequisites

Docker & Docker Compose

A running Music Assistant instance

A long-lived Music Assistant API token

Alexa Developer Account

🔐 Music Assistant Setup

Open Music Assistant

Go to Settings → API

Create a Long-Lived Access Token

Note:

Hostname / IP

Port (default: 8095)

API token

⚙️ Configuration
.env
# Internal Docker communication
MA_BASE_URL=http://music-assistant-api:5000

# External Music Assistant connection
MA_HOST=musicassistant.local
MA_PORT=8095
MA_API_KEY=YOUR_LONG_LIVED_TOKEN

🐳 Docker Compose
docker-compose.yml
version: "3.9"

services:
  alexa-skill:
    build: ./alexa-skill
    container_name: alexa-skill
    env_file: .env
    ports:
      - "5985:8080"
    depends_on:
      - music-assistant-api

  music-assistant-api:
    build: ./music-assistant-api
    container_name: music-assistant-api
    env_file: .env
    ports:
      - "5000:5000"

▶️ Start the Services
docker compose up --build

Service Endpoints
Service	URL
Alexa Skill Endpoint	http://localhost:5985
MA Alexa API	http://localhost:5000
🗣 Alexa Skill Setup
1. Create Skill

Alexa Developer Console → Create Skill

Skill type: Custom

Backend: HTTPS endpoint

Language: de-DE (or adapt model)

2. Endpoint

⚠️ Alexa requires HTTPS for real devices

Use one of:

Reverse proxy (Caddy / Traefik)

Cloudflare Tunnel

Public HTTPS endpoint

Example:

https://alexa.example.com/

3. Interaction Model

Import:

interactionModels/custom/de-DE.json

🎵 Playback Flow
▶️ Play

Alexa requests stream

MA queue is queried

Alexa receives direct MA stream URL

⏸ Pause

Alexa stops immediately

Offset is sent to MA

MA pauses the queue

▶️ Resume

Alexa requests stream

MA seeks to last offset

Playback resumes exactly

🚫 What This Project Does NOT Do

❌ No AlexaPy

❌ No Alexa Media Player

❌ No polling or hacks

❌ No dummy streams

⚠️ Notes & Limitations

Alexa requires public HTTPS for physical devices

Multi-room Alexa groups require additional handling

Offset accuracy depends on Alexa AudioPlayer events

🧪 Testing

Use Alexa Developer Console Simulator

Watch logs via:

docker compose logs -f

🛠 Troubleshooting
Alexa says “The skill is not responding”

HTTPS missing or invalid

Endpoint unreachable from internet

Playback does not resume correctly

Check MA API token permissions

Verify queue IDs

Inspect /api/alexa/state logs

🚀 Future Improvements

Automatic next-track handling

Persistent state storage

Speaker group awareness

Full Alexa Smart Home integration

📜 License

MIT License