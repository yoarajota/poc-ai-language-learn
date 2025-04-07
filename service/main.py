import asyncio
import websockets
import ssl
import os
from dotenv import load_dotenv, find_dotenv
from models.whisper import WhisperModel

# Load environment variables
load_dotenv(find_dotenv())
PORT = int(os.getenv("WS_SERVER_PORT", 8765))
CERT_FILE = os.getenv("SSL_CERT_FILE", "path/to/cert.pem")
KEY_FILE = os.getenv("SSL_KEY_FILE", "path/to/key.pem")
ENV = os.getenv("ENV", "development")

Whisper = WhisperModel()

async def process_audio(audio_data_in_bytes):
    print(f"Received audio data of length: {len(audio_data_in_bytes)} bytes")

    Whisper.transcribe(audio_data_in_bytes)

    return "Audio processed successfully"

async def handler(websocket):
    print("Client connected")
    
    try:
        async for message in websocket:
            if isinstance(message, bytes): 
                response = await process_audio(message)
                await websocket.send(response)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        print("Client disconnected")

async def main():
    print(f"Starting WebSocket server on port {PORT}")
    print("Warning: SSL is only enabled in production mode.")

    ssl_context = None
    if ENV != "development":        
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    async with websockets.serve(handler, "localhost", PORT, ssl=ssl_context):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
