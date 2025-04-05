from websocket import WebSocketApp
from threading import Thread
import time
import os
from dotenv import load_dotenv, find_dotenv

class WSClient:
    def __init__(self, on_message):

        load_dotenv(find_dotenv())
        self.url = os.getenv("WS_SERVER")
        self.on_message = on_message
        
        self.ws = WebSocketApp(self.url,
                               on_message=self._on_message,
                               on_error=self._on_error,
                               on_close=self._on_close)
        
        print(f"Connecting to WebSocket server... ${self.url}")	

    def _on_message(self, ws, message):
        self.on_message(message)

    def _on_error(self, ws, error):
        print("WebSocket error:", error)

    def _on_close(self, ws, code, msg):
        print("WebSocket closed")

    def send_audio(self, audio_data):
        if self.ws.sock and self.ws.sock.connected:
            self.ws.send(audio_data, opcode=0x2)

    def run_forever(self):
        Thread(target=lambda: self.ws.run_forever(), daemon=True).start()
