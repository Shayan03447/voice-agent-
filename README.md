# Airbridge Voice Agent

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-Whisper%20%7C%20GPT-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)

> A real-time AI voice agent that handles inbound phone calls and local microphone sessions — transcribes Urdu speech, reasons with GPT, and responds with natural-sounding voice synthesis.

---

## Overview

Airbridge Voice Agent is a production-grade, asynchronous voice AI pipeline built on FastAPI and WebSockets. It accepts live audio streams from Twilio phone calls or a local microphone, transcribes speech to text using OpenAI Whisper (optimized for Urdu), processes the conversation with a GPT language model, and replies via ElevenLabs text-to-speech synthesis.

The agent is designed for real-world business use cases including:

- Inbound customer call handling
- Appointment booking and calendar management
- Lead qualification and CRM handoff
- Inventory queries
- WhatsApp follow-up notifications

---

## Features

- **Real-time WebSocket audio streaming** — low-latency PCM audio ingestion over `ws://`
- **Automatic speech buffering** — chunks are accumulated and flushed every 10 frames for optimal STT throughput
- **Urdu STT** — OpenAI Whisper (`whisper-1`) with `language=ur` for native Urdu transcription
- **GPT-powered conversation** — async OpenAI GPT with full tool-call support
- **ElevenLabs TTS** — natural voice synthesis streamed back to the caller
- **Twilio telephony** — TwiML integration for inbound PSTN phone calls
- **Google Calendar** — appointment booking and availability checks
- **WhatsApp notifications** — follow-up messages to callers after the call
- **PostgreSQL persistence** — call logs, leads, appointments, and inventory stored via SQLAlchemy + asyncpg
- **Structured logging** — timestamped, level-tagged logs across every module
- **Pydantic settings** — all secrets loaded from `.env` with validation at startup

---

## Architecture

```
                     ┌──────────────┐     ┌──────────────┐
                     │  Twilio PSTN │     │  client.py   │
                     │  (phone call)│     │  (local mic) │
                     └──────┬───────┘     └──────┬───────┘
                            │  raw PCM bytes      │
                            └─────────┬───────────┘
                                      ▼
                         ┌────────────────────────┐
                         │  WebSocket             │
                         │  /voice/incoming       │
                         │  (media_stream.py)     │
                         └────────────┬───────────┘
                                      ▼
                         ┌────────────────────────┐
                         │  AudioPipeline         │
                         │  (buffer every 10      │
                         │   chunks → flush)      │
                         └────────────┬───────────┘
                                      ▼
                         ┌────────────────────────┐
                         │  STTAdapter            │
                         │  OpenAI Whisper (ur)   │
                         └────────────┬───────────┘
                                      ▼
                         ┌────────────────────────┐
                         │  LLMAdaptor            │
                         │  OpenAI GPT            │
                         │  (tool calls enabled)  │
                         └──┬────────┬────────┬───┘
                            │        │        │
               ┌────────────┘   ┌────┘   ┌───┘
               ▼                ▼        ▼
        ┌─────────────┐  ┌──────────┐  ┌──────────────┐
        │   Booking   │  │ Calendar │  │   WhatsApp   │
        │   / CRM     │  │ (Google) │  │ Notification │
        └─────────────┘  └──────────┘  └──────────────┘
                                      ▼
                         ┌────────────────────────┐
                         │  ElevenLabs TTS        │
                         │  (voice synthesis)     │
                         └────────────┬───────────┘
                                      ▼
                         ┌────────────────────────┐
                         │  SpeakerOutput /       │
                         │  Twilio media stream   │
                         └────────────────────────┘
```

---

## Tech Stack

| Package | Version | Role |
|---|---|---|
| `fastapi` | latest | Async web framework |
| `uvicorn[standard]` | latest | ASGI production server |
| `openai` | latest | Whisper STT + GPT LLM |
| `elevenlabs` | latest | Text-to-speech synthesis |
| `deepgram-sdk` | latest | Alternative STT provider |
| `twilio` | latest | PSTN telephony integration |
| `pyaudio` | latest | Local microphone and speaker I/O |
| `pydantic-settings` | latest | Environment variable validation |
| `python-dotenv` | latest | `.env` file loading |
| `sqlalchemy` | latest | Async ORM |
| `asyncpg` | latest | Async PostgreSQL driver |
| `alembic` | latest | Database migrations |
| `google-api-python-client` | latest | Google Calendar API |
| `httpx` | latest | Async HTTP client |

---

## Prerequisites

- **Python 3.11+**
- **PostgreSQL 15+** — running and accessible
- **API keys** for:
  - [OpenAI](https://platform.openai.com/api-keys) (required)
  - [ElevenLabs](https://elevenlabs.io) (for TTS)
  - [Deepgram](https://deepgram.com) (alternative STT)
  - [Twilio](https://console.twilio.com) (for phone calls)
  - [Google Cloud](https://console.cloud.google.com) with Calendar API enabled

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/shayan-ali/airbridge-voice-agent.git
cd airbridge-voice-agent

# 2. Create and activate a virtual environment
python -m venv myvenv

# Windows
myvenv\Scripts\activate

# macOS / Linux
source myvenv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

| Variable | Required | Description | Where to get it |
|---|---|---|---|
| `OPENAI_API_KEY` | Yes | OpenAI API key for Whisper STT and GPT | [platform.openai.com](https://platform.openai.com/api-keys) |
| `DEEPGRAM_API_KEY` | No | Deepgram API key (alternative STT) | [deepgram.com](https://deepgram.com) |
| `ELEVENLABS_API_KEY` | No | ElevenLabs API key for TTS | [elevenlabs.io](https://elevenlabs.io) |
| `ELEVENLABS_VOICE_ID` | No | ID of the ElevenLabs voice to use | ElevenLabs dashboard |
| `DATABASE_URL` | No | PostgreSQL connection string | Your DB host |
| `DEBUG` | No | Enable debug logging (`true`/`false`) | — |

Example `.env`:

```env
OPENAI_API_KEY=sk-...
DEEPGRAM_API_KEY=...
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/airbridge
DEBUG=false
```

---

## Running Locally

### Start the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is now available at `http://localhost:8000`.

### Test with local microphone

In a second terminal, run the included test client to stream your microphone directly to the agent:

```bash
python client.py
```

The client connects to `ws://127.0.0.1:8000/voice/incoming` and streams raw PCM audio in real time. Press `Ctrl+C` to stop.

### Database migrations

```bash
alembic upgrade head
```

---

## Running in Production

### Uvicorn with multiple workers

```bash
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --loop uvloop \
  --http h11
```

### Recommended: Nginx reverse proxy

Place Nginx in front of uvicorn to handle SSL termination and WebSocket upgrades:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate     /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host $host;
        proxy_read_timeout 3600s;
    }
}
```

### Twilio webhook setup

In your [Twilio Console](https://console.twilio.com), set the **Voice webhook** on your phone number to:

```
wss://your-domain.com/voice/incoming
```

Make sure the URL uses `wss://` (secure WebSocket) in production.

### Environment hardening

- Never commit `.env` to version control — it is already in `.gitignore`
- Set `DEBUG=false` in production
- Use a secrets manager (AWS Secrets Manager, GCP Secret Manager, or HashiCorp Vault) for API keys in CI/CD pipelines
- Restrict `OPENAI_API_KEY` usage limits on the OpenAI dashboard

---

## API Reference

### `GET /`

Health check endpoint. Returns `200 OK` when the server is running.

**Response:**
```json
{ "status": "ok" }
```

---

### `WS /voice/incoming`

Real-time audio streaming endpoint. Accepts raw PCM audio bytes and processes them through the full voice pipeline.

**Protocol:** WebSocket

**Audio format expected:**
| Parameter | Value |
|---|---|
| Encoding | Raw PCM (16-bit signed integer) |
| Sample rate | 16,000 Hz |
| Channels | 1 (mono) |
| Chunk size | 1,024 bytes |

**Flow:**
1. Client connects and sends continuous 1024-byte audio chunks
2. Server buffers 10 chunks, then flushes to STT (Whisper)
3. Transcript is sent to GPT for a response
4. GPT response is synthesized by ElevenLabs and streamed back
5. Server sends `"ok"` as a text acknowledgment after each received chunk

**Disconnect:** Server handles `WebSocketDisconnect` gracefully and cleans up the session.

---

## Project Structure

```
voice-agent/
│
├── app/
│   ├── main.py                          # FastAPI app entry point
│   │
│   ├── api/
│   │   ├── health.py                    # Dedicated health endpoint
│   │   └── websockets/
│   │       └── media_stream.py          # WS /voice/incoming handler
│   │
│   ├── application/
│   │   ├── ai_service.py                # Orchestrator: STT → LLM → TTS
│   │   ├── audio_pipeline.py            # Chunk buffering and flush logic
│   │   └── buffer.py                    # In-memory audio byte accumulator
│   │
│   ├── adapters/
│   │   ├── audio/
│   │   │   ├── microphone.py            # Local mic capture (AsyncGenerator)
│   │   │   └── speaker.py              # Local speaker playback
│   │   ├── llm/
│   │   │   └── openai.py               # Async GPT client + ToolCalls dataclass
│   │   ├── speech/
│   │   │   ├── deepgram.py             # OpenAI Whisper STT (Urdu)
│   │   │   └── elevenlabs.py           # ElevenLabs TTS
│   │   ├── telephony/
│   │   │   └── twilio.py               # TwiML response generation
│   │   ├── calendar/
│   │   │   └── google_calendar.py      # Google Calendar booking
│   │   └── notifications/
│   │       └── whatsapp.py             # WhatsApp follow-up messages
│   │
│   ├── domain/
│   │   ├── models/                      # Data models: Call, Lead, Appointment, Inventory
│   │   ├── conversation/               # Prompts, session state, state machine
│   │   └── tools/                      # LLM tool definitions: booking, handoff, qualification
│   │
│   ├── infrastructure/
│   │   ├── config.py                    # Pydantic settings from .env
│   │   ├── logger.py                    # Structured logging factory
│   │   └── database/                   # SQLAlchemy models, connection, repositories
│   │
│   └── shared/
│       ├── constants.py                 # Project-wide constants
│       ├── exceptions.py               # Custom exception classes
│       └── helpers.py                  # Utility functions
│
├── client.py                            # Local mic test client (WebSocket)
├── data/
│   └── inventory.json                   # Product/inventory seed data
├── scripts/
│   └── seed_db.py                       # Database seeding script
├── tests/                               # Test suite
│
├── .env                                 # Local secrets (not committed)
├── .env.example                         # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## License

MIT License — Copyright (c) 2026 Shayan Ali

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
