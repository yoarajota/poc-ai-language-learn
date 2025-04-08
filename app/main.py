import sys
import pyaudio
import io
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor, QPalette
from ws_client import WSClient

class Communicator(QObject):
    new_message = pyqtSignal(str)

class RealTimeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Phrases")
        self.setGeometry(300, 300, 600, 500)

        layout = QVBoxLayout()
        header_layout = QHBoxLayout()

        self.label = QLabel("📡 Real-Time Pronunciation Feedback")
        self.label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #FFFFFF; margin-bottom: 10px;")
        header_layout.addWidget(self.label)

        layout.addLayout(header_layout)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFont(QFont("Courier", 12))
        self.text_area.setStyleSheet(
            "background-color: #2C3E50; border: 1px solid #34495E; padding: 10px; color: #ECF0F1;"
        )
        layout.addWidget(self.text_area)

        self.audio_button = QPushButton("🎙️ Start Streaming")
        self.audio_button.setStyleSheet("background-color: #34495E; color: #ECF0F1; padding: 10px;")
        self.audio_button.clicked.connect(self.toggle_audio_streaming)
        layout.addWidget(self.audio_button)

        self.setLayout(layout)

        self.comm = Communicator()
        self.comm.new_message.connect(self.display_phrase)
        self.ws_client = WSClient(self.on_websocket_message)

        self.audio_stream = None
        self.is_streaming = False
        self.audio_buffer = io.BytesIO()  # Buffer para armazenar os dados de áudio

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1C2833"))
        self.setPalette(palette)

        print("App initialized.")

    def display_phrase(self, phrase):
        self.text_area.append(f"> {phrase}")

    def toggle_audio_streaming(self):
        if self.is_streaming:
            self.stop_audio_streaming()
        else:
            self.start_audio_streaming()

    def start_audio_streaming(self):
        print("Starting audio streaming...")

        self.audio_button.setText("⏹️ Stop Streaming")
        self.is_streaming = True

        self.audio = pyaudio.PyAudio()
        self.audio_stream = self.audio.open(format=pyaudio.paInt16,
                                            channels=1,
                                            rate=16000,
                                            input=True,
                                            frames_per_buffer=1024,
                                            stream_callback=self.audio_callback)
        self.audio_stream.start_stream()

    def stop_audio_streaming(self):
        self.audio_button.setText("🎙️ Start Streaming")
        self.is_streaming = False

        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.audio:
            self.audio.terminate()

        # Limpa o buffer ao parar o streaming
        self.audio_buffer.seek(0)
        self.audio_buffer.truncate(0)

    def audio_callback(self, in_data, frame_count, time_info, status):
        """
        Callback de áudio para capturar dados e enviá-los ao backend.
        """
        if self.is_streaming:
            self.audio_buffer.write(in_data)

            self.ws_client.send_audio(self.audio_buffer.getvalue())

            self.audio_buffer.seek(0)
            self.audio_buffer.truncate(0)

        return (in_data, pyaudio.paContinue)

    def on_websocket_message(self, message):
        self.comm.new_message.emit(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealTimeApp()
    window.show()
    sys.exit(app.exec())