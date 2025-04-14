from speechbrain.inference.text import GraphemeToPhoneme
import platform

class SoundChoiceG2PModel:
    def __init__(self):

        if platform.system() == "Windows":
            download_options = {"save_folder": "pretrained_models/soundchoice-g2p", "overwrite": False, "symlink_strategy": "copy"}
        else:
            download_options = {"save_folder": "pretrained_models/soundchoice-g2p", "overwrite": False}
            
        self.g2p = GraphemeToPhoneme.from_hparams(
            source="speechbrain/soundchoice-g2p", 
            savedir="pretrained_models/soundchoice-g2p",
            download_options=download_options
        )

    def text_to_phonemes(self, text):
        if not text:
            return []
        
        return self.g2p(text)
    
    def batch_to_phonemes(self, text_list):
        if not text_list:
            return []
        
        return [self.text_to_phonemes(text) for text in text_list]
    
    def get_phonetic_representation(self, text):
        phonemes = self.text_to_phonemes(text)
        return ' '.join(phonemes).replace('  ', ' | ')