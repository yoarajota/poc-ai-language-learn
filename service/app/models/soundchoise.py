from speechbrain.inference.text import GraphemeToPhoneme
import os

class SoundChoiceG2PModel:
    def __init__(self):
        print("Loading SoundChoice G2P model...")
        try:
            savedir = os.path.abspath("pretrained_models/soundchoice-g2p")
            os.makedirs(savedir, exist_ok=True)
            
            self.g2p = GraphemeToPhoneme.from_hparams(
                source="speechbrain/soundchoice-g2p", 
                savedir=savedir,
                run_opts={"device": "cpu"}
            )
            
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.g2p = None

    def text_to_phonemes(self, text):
        if not text or self.g2p is None:
            if self.g2p is None:
                print("G2P model is not loaded.")

            return []
        
        try:
            phonemes = self.g2p(text)
            
            if isinstance(phonemes, tuple) and len(phonemes) > 0:
                return phonemes[0]
            
            return phonemes
        except Exception as e:
            print(f"Error in text_to_phonemes: {e}")
            return []
    
    def get_phonetic_representation(self, text):
        if not text or self.g2p is None:
            return ""
        
        try:
            phonemes = self.text_to_phonemes(text)
            if not phonemes:
                return ""
            
            if isinstance(phonemes, list):
                return ' '.join(phonemes).replace('  ', ' | ')
            else:
                return str(phonemes)
        except Exception as e:
            print(f"Error in get_phonetic_representation: {e}")
            return ""