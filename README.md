# Voice AI Agent

## Project Overview  
Voice AI Agent is a Dockerized FastAPI application that transforms incoming phone calls into an interactive, AI-driven conversation. It leverages Twilio for telephony, OpenAI’s Whisper for speech-to-text, GPT-3.5-turbo for natural language understanding and response generation, and a TTS engine for playback—all exposed securely via an ngrok tunnel.

## Key Features  
- **Real-Time Call Handling**  
  Answer calls automatically and prompt the caller with a friendly greeting.  
- **Accurate Transcription**  
  Record and send audio to Whisper for fast, high-fidelity speech recognition.  
- **Contextual AI Dialogue**  
  Maintain session history and use GPT-3.5-turbo to generate coherent, context-aware replies.  
- **Natural TTS Playback**  
  Convert AI responses into speech (TTS-1) and stream back over the call.  
- **Flexible Deployment**  
  Run locally for development or package into Docker for consistent, cloud-ready deployment.

## Architecture and Workflow  
1. **Incoming Call** → Twilio POSTs to `POST /twilio/voice`.  
2. **Greeting & Record** → FastAPI returns TwiML to greet and record the caller.  
3. **Download & Transcribe** → Fetch the recording, send to Whisper, retrieve text.  
4. **Generate Reply** → Append to history, call GPT-3.5-turbo, receive response text.  
5. **Synthesize & Play** → Convert text to speech, store as `response.mp3`, instruct Twilio to play it.  
6. **Loop or Hang Up** → Redirect back to `/twilio/voice` until an exit phrase is detected.

## Benefits  
- **Plug-and-Play**: Minimal configuration—just an `.env` and ngrok URL.  
- **Scalable & Portable**: Docker container runs identically anywhere.  
- **Extensible**: Swap models, tweak timeouts, or integrate additional services in minutes.

## Target Audience  
- **Developers & AI Enthusiasts** exploring voice-first interfaces.  
- **Prototype Builders** adding conversational IVR to their applications.  
- **Educators & Students** learning about speech-to-text, NLP, and API orchestration.

## Getting Started  
1. Clone the repo and navigate inside:  
   ```bash
   git clone https://github.com/<your-username>/Voice-AI-Agent.git
   cd Voice-AI-Agent
