# pip install speechbrain
# pip install transformers

# https://huggingface.co/speechbrain/soundchoice-g2p

from speechbrain.inference.text import GraphemeToPhoneme
import time

class SoundChoiceG2P:
    def __init__(self, use_cuda=False):
        print("Carregando modelo SoundChoice G2P...")
        start_time = time.time()
        
        run_opts = {"device": "cuda"} if use_cuda else {"device": "cpu"}
        self.model = GraphemeToPhoneme.from_hparams(
            source="speechbrain/soundchoice-g2p",
            run_opts=run_opts
        )
        
        load_time = time.time() - start_time
        print(f"Modelo carregado em {load_time:.2f} segundos.")
    
    def text_to_phonemes(self, text):
        if not text:
            return []
        
        return self.model(text)
    
    def batch_to_phonemes(self, text_list):
        if not text_list:
            return []
        
        return [self.text_to_phonemes(text) for text in text_list]
    
    def get_phonetic_representation(self, text):
        phonemes = self.text_to_phonemes(text)
        return ' '.join(phonemes).replace('  ', ' | ')