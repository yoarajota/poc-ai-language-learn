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

async def process_audio(audio_data_in_bytes):
    transcription = Whisper.transcribe(audio_data_in_bytes)

    # Check grammar and correct if necessary
    checked = Grammar.correct_grammar(transcription)

    if checked != transcription:
        print("Grammar correction applied")
        checked_phonemes = SoundChoiceG2P.text_to_phonemes(checked)

        # Generate audio for the corrected text
        audio_buffer = io.BytesIO()
        tts = gtts.gTTS(checked_phonemes, lang="en", slow=False)
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return {
            "audio": audio_buffer.getvalue(),
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

            result = await process_audio(message)

            if result:
                await websocket.send_json(result)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()