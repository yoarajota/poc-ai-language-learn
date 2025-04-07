import websocket
import os
from dotenv import load_dotenv, find_dotenv
from threading import Thread
import time

class WSClient:
    def __init__(self, on_message):
        load_dotenv(find_dotenv())
        self.url = os.getenv("WS_SERVER")
        if not self.url:
            raise ValueError("WebSocket server URL (WS_SERVER) is not set in the environment variables.")
        
        self.on_message = on_message
        self.ws = None
        self.is_running = False

        print(f"WebSocket client initialized for server at {self.url}.")
        self.run_forever()

    def _connect(self):
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(self.url)
            print("Connected to WebSocket server.")
        except Exception as e:
            print(f"Failed to connect to WebSocket server: {e}")
            self.ws = None

    def _listen(self):
        try:
            while self.is_running and self.ws:
                message = self.ws.recv()
                self.on_message(message)
        except Exception as e:
            print(f"Error while listening to WebSocket: {e}")
            self.ws = None

    def send_audio(self, audio_data):
        try:
            if self.ws:
                self.ws.send(audio_data, opcode=websocket.ABNF.OPCODE_BINARY)
            else:
                print("WebSocket is not connected. Unable to send audio.")
        except Exception as e:
            print(f"Error sending audio: {e}")

    def run_forever(self):
        def run():
            self.is_running = True
            while self.is_running:
                if not self.ws:
                    print("Attempting to connect to WebSocket server...")
                    self._connect()
                if self.ws:
                    self._listen()
                print("Reconnecting in 5 seconds...")
                time.sleep(5)

        Thread(target=run, daemon=True).start()

    def close(self):
        self.is_running = False
        if self.ws:
            try:
                self.ws.close()
                print("WebSocket connection closed.")
            except Exception as e:
                print(f"Error closing WebSocket: {e}")