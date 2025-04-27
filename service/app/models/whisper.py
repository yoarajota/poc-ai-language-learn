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

        time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        temp_audio_path = f"models/whisper/temp/{time}.wav"
        
        if not os.path.exists("models/whisper/temp"):
            os.makedirs("models/whisper/temp")

        with open(temp_audio_path, "wb") as f:
            sf.write(f, audio, sample_rate, format='WAV')


        result = self.model.transcribe(audio, language="en", fp16=False)

        return result["text"]