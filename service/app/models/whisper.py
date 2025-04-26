import whisper
import numpy as np
import io
import soundfile as sf
import os
import datetime

class WhisperModel:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_bytes, sample_rate=16000):

        audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        result = self.model.transcribe(audio, language="en", fp16=False)

        return result["text"]