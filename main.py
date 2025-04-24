from fastapi import FastAPI, Request
from fastapi.responses import Response, FileResponse
from openai import OpenAI
from dotenv import load_dotenv
import requests, os, time

# ─── CONFIGURATION ───────────────────────────────────────────────────────────────
load_dotenv()
client       = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TWILIO_SID   = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
NGROK_URL    = os.getenv("NGROK_URL")

app = FastAPI()

# ─── IN-MEMORY SESSIONS ───────────────────────────────────────────────────────────
# map CallSid → [{role: "user"|"assistant", content: "..."}]
sessions: dict[str, list[dict]] = {}
EXIT_PHRASES = [
    "bye", "goodbye", "talk to you later", "see you",
    "thank you", "that’s all", "i’m done"
]

# ─── 1) FIRST WEBHOOK: ANSWER & RECORD ────────────────────────────────────────────
@app.post("/twilio/voice")
async def voice(request: Request):
    form    = await request.form()
    call_sid = form.get("CallSid")
    if not call_sid:
        return Response("<Response><Say>Missing CallSid.</Say></Response>",
                        media_type="application/xml")

    history = sessions.setdefault(call_sid, [])
    # only play the greeting if this is truly the first turn
    greeting = ""
    if not history:
        greeting = (
          '<Say voice="alice">'
          "Hello! I’m your voice assistant. Please speak after the beep."
          "</Say>"
        )

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  {greeting}
  <Record
    maxLength="30"
    timeout="3"
    action="{NGROK_URL}/twilio/handle-recording"
    method="POST"
    playBeep="true"/>
</Response>"""
    return Response(content=xml, media_type="application/xml")


# ─── 2) RECORDING CALLBACK: TRANSCRIBE → CHAT → TTS → RESPOND ──────────────────────
@app.post("/twilio/handle-recording")
async def handle_recording(request: Request):
    form          = await request.form()
    call_sid      = form.get("CallSid")
    recording_url = form.get("RecordingUrl")

    if not call_sid or not recording_url:
        return Response("<Response><Say>Sorry, something went wrong.</Say></Response>",
                        media_type="application/xml")

    history = sessions.setdefault(call_sid, [])
    print("🎙️ Recording URL:", recording_url)

    # download the .wav
    for _ in range(5):
        resp = requests.get(recording_url + ".wav",
                            auth=(TWILIO_SID, TWILIO_TOKEN))
        if resp.status_code == 200:
            break
        time.sleep(1)
    else:
        return Response(
          "<Response><Say>Couldn’t download your recording.</Say></Response>",
          media_type="application/xml"
        )

    with open("recording.wav", "wb") as f:
        f.write(resp.content)

    # Whisper STT
    with open("recording.wav", "rb") as audio_f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=audio_f
        )
    user_text = transcript.text.strip()
    print("📝 Transcription:", user_text)

    # if user says “bye” *and* we already had a convo, hang up
    if history and any(p in user_text.lower() for p in EXIT_PHRASES):
        sessions.pop(call_sid, None)
        return Response(
          """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say>Goodbye!</Say>
  <Hangup/>
</Response>""",
          media_type="application/xml"
        )

    # add the user message, call Chat API
    history.append({"role": "user", "content": user_text})
    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    reply = chat.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": reply})
    print("🤖 GPT Reply:", reply)

    # TTS → response.mp3
    client.audio.speech.create(
        model="tts-1", voice="nova", input=reply
    ).stream_to_file("response.mp3")
    print("🔊 response.mp3 ready")

    # tell Twilio to play it, then return to /twilio/voice (with no greeting next time)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Play>{NGROK_URL}/play-response</Play>
  <Redirect>{NGROK_URL}/twilio/voice</Redirect>
</Response>"""
    return Response(content=xml, media_type="application/xml")


# ─── 3) SERVE YOUR MP3 ──────────────────────────────────────────────────────────
@app.get("/play-response")
def play_response():
    if not os.path.exists("response.mp3"):
        return Response("<Response><Say>Audio not found.</Say></Response>",
                        media_type="application/xml")
    return FileResponse("response.mp3", media_type="audio/mpeg")
