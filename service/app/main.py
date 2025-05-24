from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

app = FastAPI()

async def handle_audio(audio_data_in_bytes):
    print("Received audio data")

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