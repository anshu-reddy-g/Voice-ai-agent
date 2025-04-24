# Voice AI Agent
A programmable voice assistant built with FastAPI, Ngrok, Twilio & OpenAI.

![Call Demo](docs/demo.gif)

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker](#docker)
- [Deploying](#deploying)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Features
- ☎️  Receive & record phone calls  
- 📝  Transcribe with Whisper  
- 🤖  Chat with GPT-3.5-turbo  
- 🔊  Text-to-speech replies via OpenAI TTS  
- 🚀  Easy Docker + Ngrok setup  

## Getting Started
```bash
git clone https://github.com/anshu-reddy-g/Voice-ai-agent.git
cd Voice-ai-agent
cp .env.example .env
# fill in your .env secrets, then:
docker-compose up --build
