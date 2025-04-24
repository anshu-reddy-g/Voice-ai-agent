# Voice AI Agent

A FastAPI-based voice assistant that uses OpenAI's Whisper for transcription, GPT-3.5 for conversational responses, and Twilio + ngrok for telephony integration.

## Features

- **Record & Transcribe**: Records caller audio via Twilio, transcribes with Whisper (`whisper-1`).
- **Conversational AI**: Maintains per-call history and responds using GPT-3.5-turbo.
- **Text-to-Speech**: Converts GPT replies to speech (`tts-1`, voice `nova`).
- **Session Management**: Detects exit phrases to end calls gracefully.
- **Dockerized**: Run in a container for consistent deployment.

## Prerequisites

- **Git** and a GitHub repository.
- **Docker** & **Docker Compose** (or Docker CLI).
- **Twilio** account with a phone number.
- **ngrok** (or any public tunneling solution).
- **OpenAI** API key with access to Whisper and TTS.

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<USERNAME>/<REPO>.git
   cd <REPO>
   ```

2. **Create `.env`**
   Copy `.env.example` to `.env` and fill in your credentials:
   ```ini
   OPENAI_API_KEY=sk-...
   TWILIO_SID=AC...
   TWILIO_AUTH_TOKEN=...
   NGROK_URL=https://xxxx.ngrok.io
   ```

3. **Prepare Docker image**
   ```bash
   docker build -t voice-ai-agent .
   ```

4. **Run container**
   ```bash
   docker run --rm -it \
     -v "$PWD/voice-agent-key.json:/app/voice-agent-key.json:ro" \
     --env-file .env \
     -p 8000:8000 \
     voice-ai-agent
   ```

5. **Start ngrok**
   ```bash
   ngrok http 8000
   ```
   Update your `.env` with the displayed HTTPS URL for `NGROK_URL`.

6. **Configure Twilio Webhook**
   In your Twilio console, set your phone number's **Voice & Fax** webhook to:
   ```plaintext
   https://<YOUR_NGROK_URL>/twilio/voice
   ```

## Usage

- **Make a call** to your Twilio number.
- **Speak** after the beep.
- The agent will transcribe, generate a reply, and play it back.
- Say an **exit phrase** (e.g. "bye") to end the call.

## Demo

To capture a quick screencast:

- **macOS**: Download LICEcap from its homepage: [https://www.cockos.com/licecap/](https://www.cockos.com/licecap/)
- **Linux**: Get Peek releases on GitHub: [https://github.com/phw/peek/releases](https://github.com/phw/peek/releases) or install via package manager:
  ```bash
  sudo apt install peek
  ```

Record your terminal and/or phone emulator to a GIF, save it at `media/demo.gif`, and embed:

```md
## Live Demo

![Quick GIF showing the full call flow](media/demo.gif)
```

## Contributing

1. Fork and clone.
2. Create a branch: `git checkout -b feature/awesome`.
3. Commit: `git commit -m "Add awesome feature"`.
4. Push: `git push origin feature/awesome`.
5. Open a Pull Request.

## License

MIT © Your Name

