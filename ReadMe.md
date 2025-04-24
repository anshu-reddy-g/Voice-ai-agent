---
title: "Voice AI Agent"
author: "Your Name"
date: "`r format(Sys.Date(), '%B %d, %Y')`"
output: github_document
---

# Voice AI Agent

A Dockerized FastAPI application that turns phone calls into a live conversational AI using Twilio, OpenAI’s Whisper for speech-to-text, GPT-3.5-turbo for chat, and ngrok for public tunneling.

---

## 🚀 Features

- **Answer incoming calls** via Twilio webhook  
- **Record caller’s voice** and transcribe with Whisper  
- **Generate contextual AI responses** with GPT-3.5-turbo  
- **Convert text replies to speech (TTS)** and play back  
- **Persistent conversation history** per session  
- **Local development** or **Docker** deployment  

---

## 📂 Repository Structure

```
.
├── main.py              # FastAPI application  
├── Dockerfile           # Container build instructions  
├── requirements.txt     # Python dependencies  
├── .env.example         # Sample environment file  
└── README.Rmd           # This guide  
```

---

## 🔧 Prerequisites

- Python 3.8+  
- Docker & Docker CLI  
- Twilio account & phone number  
- OpenAI API key  
- ngrok account (or any tunnel service)  
- (Optional) GCP service account JSON for uploads  

---

## ⚙️ Setup & Local Development

1. **Clone the repo**  
   ```bash
   git clone https://github.com/<your-username>/Voice-ai-agent.git
   cd Voice-ai-agent
   ```

2. **Configure your environment**  
   ```bash
   cp .env.example .env
   ```  
   Edit `.env` with your credentials:
   ```ini
   OPENAI_API_KEY=your_openai_key  
   TWILIO_SID=your_twilio_sid  
   TWILIO_AUTH_TOKEN=your_twilio_token  
   NGROK_URL=https://your-ngrok-url  
   GCP_BUCKET_NAME=your_gcp_bucket  
   GOOGLE_APPLICATION_CREDENTIALS=/app/voice-agent-key.json  
   ```

3. **Install dependencies**  
   ```bash
   python3 -m venv venv  
   source venv/bin/activate  
   pip install -r requirements.txt  
   ```

4. **Run the app**  
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Expose with ngrok**  
   ```bash
   ngrok http 8000
   ```  
   Copy the HTTPS URL and update `NGROK_URL` in your `.env`.

6. **Configure your Twilio webhook**  
   In the Twilio Console → Phone Numbers → Your Number → Voice & Fax → Webhook:

   - **Method:** POST  
   - **URL:** `https://<your-ngrok-url>/twilio/voice`  

---

## 🐳 Docker Deployment

1. **Build the Docker image**  
   ```bash
   docker build -t voice-ai-agent .
   ```

2. **Run the container**  
   ```bash
   docker run --rm -it \
     -v "$PWD/voice-agent-key.json:/app/voice-agent-key.json:ro" \
     --env-file .env \
     -p 8000:8000 \
     voice-ai-agent
   ```

3. **Reconfigure ngrok & Twilio** as above, pointing at port 8000.

---

## ✅ Testing Endpoints

- **Simulate a call**  
  ```bash
  curl -X POST http://localhost:8000/twilio/voice
  ```

- **Fetch the generated audio**  
  ```bash
  curl http://localhost:8000/play-response --output response.mp3
  ```

---

## 🤝 Contributing

1. Fork the repo  
2. Create a branch:  
   ```bash
   git checkout -b feature/foo
   ```  
3. Commit your changes:  
   ```bash
   git commit -m "Add foo"
   ```  
4. Push:  
   ```bash
   git push origin feature/foo
   ```  
5. Open a Pull Request  

---

## 📄 License
MIT © Anshu Goli

This project is licensed under the MIT License.
