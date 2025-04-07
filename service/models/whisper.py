import whisper
import numpy as np
import io
import soundfile as sf

class WhisperModel:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_bytes, sample_rate=16000, channels=1, subtype="PCM_16"):
        """
        Transcribe audio from bytes using Whisper.
        Handles both raw PCM data and standard audio formats.
        """
        try:
            audio, file_sample_rate = sf.read(io.BytesIO(audio_bytes), dtype="float32")
        except sf.LibsndfileError:
            print("Unrecognized audio format. Attempting to process as raw PCM data...")
            audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            file_sample_rate = sample_rate

        if file_sample_rate != 16000:
            audio = whisper.audio.resample(audio, file_sample_rate, 16000)

        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        _, probs = self.model.detect_language(mel)
        print(f"Detected language: {max(probs, key=probs.get)}")

        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)

        return result.text