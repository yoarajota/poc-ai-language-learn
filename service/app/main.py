import base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from models.whisper import WhisperModel
from models.soundchoise import SoundChoiceG2PModel
from models.grammar import GrammarCorrectionModel
import gtts
import asyncio
import io

app = FastAPI()

Whisper = WhisperModel()
SoundChoiceG2P = SoundChoiceG2PModel()
Grammar = GrammarCorrectionModel()

async def handle_audio(audio_data_in_bytes):
    print("Received audio data")

    transcription = Whisper.transcribe(audio_data_in_bytes)
    checked = Grammar.correct_grammar(transcription)

    if checked.lower().strip() != transcription.lower().strip():
        print("Grammar correction applied")

        # Generate audio for the corrected text
        audio_buffer = io.BytesIO()
        tts = gtts.gTTS(checked, lang="en", slow=False)
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")

        print("Audio generated for corrected text")
        print(transcription)

        return {
            "audio": audio_base64,
            "transcription": transcription,
            "checked": checked
        }

    return None

@app.post("/hello")
async def hello():
    return {"msg": "Hello World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    try:
        while True:
            message = await websocket.receive_bytes()

            result = await handle_audio(message)

            print("Result from handle_audio:", result)

            if result:
                await websocket.send_json(result)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()