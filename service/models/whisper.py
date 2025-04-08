import whisper
import numpy as np
import io
import soundfile as sf

class WhisperModel:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_bytes, sample_rate=16000):
        try:
            audio, file_sample_rate = sf.read(io.BytesIO(audio_bytes), dtype="float32")
        except sf.LibsndfileError:
            # If the format is not recognized, assume raw PCM data
            print("Unrecognized audio format. Attempting to process as raw PCM data...")
            audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            file_sample_rate = sample_rate

        if file_sample_rate != 16000:
            audio = whisper.audio.resample(audio, file_sample_rate, 16000)

        audio = whisper.pad_or_trim(audio)

        result = self.model.transcribe(audio, language="en", fp16=False)

        return result["text"]