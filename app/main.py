import sys
import pyaudio
import io
import numpy as np
import time
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit, 
                            QLabel, QHBoxLayout, QPushButton, QSlider, 
                            QGroupBox, QGridLayout, QProgressBar, QFrame, QLayout)
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtGui import QFont, QColor, QPalette
from ws_client import WSClient

class Communicator(QObject):
    new_message = pyqtSignal(str)
    rms_update = pyqtSignal(float)
    
class RealTimeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Phrases")
        self.setGeometry(300, 300, 700, 600)

        layout = QVBoxLayout()
        header_layout = QHBoxLayout()

        self.label = QLabel("📡 Real-Time Pronunciation Feedback")
        self.label.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #FFFFFF; margin-bottom: 10px;")
        header_layout.addWidget(self.label)

        layout.addLayout(header_layout)

        settings_box = QGroupBox("Configurações de Detecção")
        settings_box.setStyleSheet("color: #FFFFFF; background-color: #34495E; padding: 10px;")
        settings_layout = QGridLayout()
        
        self.slider_container = QFrame()
        self.slider_container.setMinimumHeight(40)
        self.slider_container.setFrameStyle(QFrame.Shape.NoFrame)
        
        overlay_container = QWidget()
        overlay_container.setLayout(QVBoxLayout())
        overlay_container.layout().setContentsMargins(0, 0, 0, 0)
        overlay_container.layout().setSpacing(0)
        
        self.rms_bar = QProgressBar()
        self.rms_bar.setRange(0, 100)
        self.rms_bar.setValue(0)
        self.rms_bar.setTextVisible(False)
        self.rms_bar.setFixedHeight(20)
        self.rms_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2C3E50;
                border: 1px solid #34495E;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #2ECC71;
                border-radius: 5px;
            }
        """)
        
        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setMinimum(1)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(10)
        self.threshold_slider.setFixedHeight(20)
        self.threshold_slider.setStyleSheet("""
            QSlider {
                background: transparent;
            }
            QSlider::groove:horizontal {
                background: transparent;
                height: 10px;
            }
            QSlider::handle:horizontal {
                background: rgba(241, 196, 15, 0.9);
                width: 8px;
                margin: -8px 0;
                border: 1px solid #34495E;
                border-radius: 3px;
                height: 24px;
            }
            QSlider::add-page:horizontal {
                background: transparent;
            }
            QSlider::sub-page:horizontal {
                background: transparent;
            }
        """)
        
        self.threshold_slider.valueChanged.connect(self.update_threshold)
        
        overlay_layout = QHBoxLayout(self.slider_container)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        
        overlay_layout.addWidget(self.rms_bar)
        
        self.threshold_slider.setParent(self.slider_container)
        self.threshold_slider.setGeometry(self.rms_bar.geometry())
        # self.threshold_slider.raise_()
        
        self.threshold_label = QLabel(f"Mic Sensibility: {0.01}")
        self.threshold_label.setStyleSheet("color: #ECF0F1;")
        
        self.rms_label = QLabel("Audio Level: 0.000")
        self.rms_label.setStyleSheet("color: #ECF0F1;")
        
        settings_layout.addWidget(self.threshold_label, 0, 0)
        settings_layout.addWidget(self.slider_container, 1, 0)
        settings_layout.addWidget(self.rms_label, 2, 0)
        
        settings_box.setLayout(settings_layout)
        layout.addWidget(settings_box)

        # Rest of your code remains unchanged
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

        # Audio and other initialization (unchanged)
        self.comm = Communicator()
        self.comm.new_message.connect(self.display_phrase)
        self.comm.rms_update.connect(self.update_rms_display)
        self.ws_client = WSClient(self.on_websocket_message)

        self.audio_stream = None
        self.is_streaming = False
        self.audio_buffer = io.BytesIO()
        self.frames_per_second = 16000 
        self.bytes_per_sample = 2 
        self.channels = 1 
        
        self.tap_threshold = 0.01
        self.silence_duration = 0.8
        self.min_phrase_duration = 1.0
        self.max_phrase_duration = 10.0
        
        self.is_speaking = False
        self.silence_start_time = 0
        self.phrase_start_time = 0
        self.last_rms = 0

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1C2833"))
        self.setPalette(palette)

        self.audio_buffer.seek(0)
        self.audio_buffer.truncate(0)

        self.audio = pyaudio.PyAudio()
        self.audio_stream = self.audio.open(format=pyaudio.paInt16,
                                            channels=self.channels,
                                            rate=self.frames_per_second,
                                            input=True,
                                            frames_per_buffer=1024,
                                            stream_callback=self.audio_callback)
        self.audio_stream.start_stream()

        print("App initialized.")

    def update_threshold(self):
        value = self.threshold_slider.value() / 1000.0
        self.tap_threshold = value
        self.threshold_label.setText(f"Mic Sensibility: {value}")
        print(f"Threshold updated to {value}")
        self.update_rms_display(self.last_rms)

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
        self.is_speaking = False

    def stop_audio_streaming(self):
        self.audio_button.setText("🎙️ Start Streaming")
        self.is_streaming = False

        self.audio_buffer.seek(0)
        self.audio_buffer.truncate(0)

    def calculate_rms(self, data):
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
    
        audio_data = audio_data / 32768.0
    
        rms = np.sqrt(np.mean(np.square(audio_data)))
        return rms

    def audio_callback(self, in_data, frame_count, time_info, status):
        current_rms = self.calculate_rms(in_data)
        self.last_rms = current_rms
        
        self.comm.rms_update.emit(current_rms)
        
        if not self.is_streaming:
            return (in_data, pyaudio.paContinue)

        self.audio_buffer.write(in_data)
        current_time = time.time()
        
        if current_rms > self.tap_threshold:
            if not self.is_speaking:
                self.is_speaking = True
                self.phrase_start_time = current_time

                buffer_size_seconds = 0.4
                pre_buffer_size = int(self.frames_per_second * self.bytes_per_sample * self.channels * buffer_size_seconds)
                
                current_pos = self.audio_buffer.tell()
                if current_pos > pre_buffer_size:
                    self.phrase_start_pos = current_pos - pre_buffer_size

                print(f"Speak: (RMS: {current_rms:.4f})")
            
            self.silence_start_time = 0
        else:
            if self.is_speaking:
                if self.silence_start_time == 0:
                    self.silence_start_time = current_time
            
                if (current_time - self.silence_start_time) >= self.silence_duration:
                    phrase_duration = current_time - self.phrase_start_time
                
                    if phrase_duration >= self.min_phrase_duration:
                        print(f"Silence: (RMS: {current_rms:.4f})")

                        self.audio_buffer.seek(self.phrase_start_pos)
                    
                        self.ws_client.send_audio(self.audio_buffer.read())
                    
                        self.audio_buffer.seek(0)
                        self.audio_buffer.truncate(0)
                    
                    self.is_speaking = False
                    self.silence_start_time = 0
                    self.phrase_start_pos = None
        
        buffer_duration = self.audio_buffer.tell() / (self.frames_per_second * self.bytes_per_sample * self.channels)
        if buffer_duration >= self.max_phrase_duration:
            self.audio_buffer.seek(0)
            self.audio_buffer.truncate(0)
            
        return (in_data, pyaudio.paContinue)

    def update_rms_display(self, rms_value):
        self.rms_label.setText(f"Audio Level: {rms_value}")
        
        rms_percent = min(int(rms_value * 1000), 100)
        self.rms_bar.setValue(rms_percent)

    def on_websocket_message(self, message):
        self.comm.new_message.emit(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealTimeApp()
    window.show()
    sys.exit(app.exec())