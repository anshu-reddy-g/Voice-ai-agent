# Voice AI Agent

## 📖 Project Overview  
Voice AI Agent is a fully Dockerized, turn-key FastAPI application that transforms ordinary phone calls into dynamic, AI-powered conversations. By seamlessly integrating Twilio’s telephony API, OpenAI’s Whisper for speech-to-text, GPT-3.5-turbo for natural language understanding and response generation, and text-to-speech for playback, this project delivers an end-to-end voice assistant you can deploy anywhere via ngrok.

## ✨ Key Features  
- **Outbound & Inbound Call Handling**  
  - Answer calls in real-time with a friendly spoken greeting  
  - Route callers into a conversational loop until they say “goodbye”  
- **Accurate Speech Recognition**  
  - Record and stream audio to OpenAI’s Whisper model for fast, highly accurate transcription  
- **Contextual AI Dialogue**  
  - Maintain session history for coherent multi-turn conversations  
  - Leverage GPT-3.5-turbo to provide intelligent, context-aware responses  
- **High-Quality TTS Playback**  
  - Convert GPT replies into natural speech (TTS-1) and play back over the call  
- **Flexible Deployment**  
  - Run locally for development or package into Docker for production  
  - Expose your local server securely via ngrok (or any reverse tunnel)

## 🏗️ Architecture & Workflow  
1. **Twilio Webhook** → FastAPI `/twilio/voice` endpoint answers the call with XML TwiML  
2. **Audio Recording** → Caller’s speech is recorded, then fetched as a WAV file  
3. **Whisper Transcription** → Audio is sent to OpenAI Whisper; result is normalized to text  
4. **GPT-3.5 Response** → Text is appended to the conversation history and sent to the chat API  
5. **TTS Generation** → GPT reply is converted to speech and streamed into `response.mp3`  
6. **Playback & Loop** → Twilio plays back the TTS file, then redirects to listen for the next user input  

## 🚀 Why You’ll Love Voice AI Agent  
- **Plug-and-Play**: Minimal configuration—just set your `.env` and ngrok URL  
- **Scalable**: Docker container runs identically on any platform or cloud service  
- **Extensible**: Easily swap models, adjust timeouts, or integrate new services  
- **Interactive Demo**: Spin up locally and call your number to see it in action  

## 🎯 Who Is This For?  
- **Developers & Enthusiasts** who want hands-on experience with real-world voice AI  
- **Prototype Builders** looking to add conversational interfaces to apps  
- **Educators & Students** exploring speech technologies, NLP, and API orchestration  

---

**Ready to get started?** Check out the [Getting Started](#-setup--local-development) section below and have your first AI-powered phone conversation in minutes!  
