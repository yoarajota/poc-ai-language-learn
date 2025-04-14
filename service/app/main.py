from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from models.whisper import WhisperModel
from models.soundchoise import SoundChoiceG2PModel
import asyncio

app = FastAPI()

Whisper = WhisperModel()
SoundChoiceG2P = SoundChoiceG2PModel()

async def process_audio(audio_data_in_bytes):
    transcription = Whisper.transcribe(audio_data_in_bytes)
    transcriptionGrapheme = SoundChoiceG2P.text_to_phonemes(transcription)

    print(transcription, transcriptionGrapheme)

    return transcription

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
            transcription = await process_audio(message)
            await websocket.send_text(transcription)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()

def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}