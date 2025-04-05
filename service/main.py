import asyncio
import websockets
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
PORT = int(os.getenv("WS_SERVER_PORT", 8765))
PORT = int(os.getenv("WS_SERVER_PORT", 8765))

async def process_audio(audio_data):
    """
    Process the received audio data.
    This is a placeholder function where you can integrate audio processing logic.
    """
    print(f"Received audio data of length: {len(audio_data)} bytes")
    # Add your audio processing logic here
    return "Audio processed successfully"

async def handler(websocket, path):
    """
    Handle incoming WebSocket connections.
    """
    print("Client connected")
    try:
        async for message in websocket:
            if isinstance(message, bytes):  # Check if the message is binary (audio data)
                response = await process_audio(message)
                await websocket.send(response)
            else:
                print(f"Received non-binary message: {message}")
                await websocket.send("Only binary audio data is supported.")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        print("Client disconnected")

async def main():
    """
    Start the WebSocket server.
    """
    print(f"Starting WebSocket server on port {PORT}...")
    async with websockets.serve(handler, "localhost", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
