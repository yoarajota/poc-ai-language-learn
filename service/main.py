from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from models.whisper import WhisperModel
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
PORT = int(os.getenv("WS_SERVER_PORT", 8765))

app = FastAPI()

Whisper = WhisperModel()

async def process_audio(audio_data_in_bytes):
    print(f"Received audio data of length: {len(audio_data_in_bytes)} bytes")
    transcription = Whisper.transcribe(audio_data_in_bytes)
    return transcription

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
        