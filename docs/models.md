# Grapheme-to-Phoneme Models:

## Try n1: SoundChoice: Grapheme-to-Phoneme Model Summary

The **SoundChoice G2P model** is a pretrained grapheme-to-phoneme (G2P) conversion tool for English, built using the **SpeechBrain** framework. It converts written text (graphemes) into phonetic representations (phonemes) and includes semantic disambiguation for improved accuracy. The model is trained on the **LibriG2P dataset**, derived from LibriSpeech Alignments and Google Wikipedia data.

### Key Features
- **Purpose**: Converts English text into phoneme sequences (e.g., "To be or not to be" → ['T', 'UW', ' ', 'B', 'IY', ...]).
- **Framework**: Built with SpeechBrain, a general-purpose speech toolkit.
- **Usage**: Supports single text or batch processing (e.g., multiple sentences at once).
- **GPU Support**: Inference can be accelerated using CUDA with `run_opts={"device":"cuda"}`.
- **Installation**: Requires `speechbrain` and `transformers` via pip.


```python
from speechbrain.inference.text import GraphemeToPhoneme

g2p = GraphemeToPhoneme.from_hparams("speechbrain/soundchoice-g2p")
text = "To be or not to be"
phonemes = g2p(text)
# Output: ['T', 'UW', ' ', 'B', 'IY', ...]
```

# Grammar Correction Models:

## Try n1: T5 Grammar Correction Model Summary

The **T5 Grammar Correction** model is a pretrained text-to-text transformer designed to correct grammatical errors in English sentences. It was trained using the **Happy Transformer** library on the **JFLEG dataset**, which is specifically designed for grammatical error correction tasks. The model generates revised versions of input text with fewer grammatical errors.

### Key Features
- **Purpose**: Corrects grammatical errors in English text (e.g., "This sentences has has bads grammar." → "This sentence has bad grammar.").
- **Framework**: Built using the T5 architecture and fine-tuned with Happy Transformer.
- **Usage**: Supports single-sentence correction with customizable settings like beam search.
- **GPU Support**: Inference can be accelerated using CUDA with `run_opts={"device":"cuda"}`.
- **Installation**: Requires happytransformer via pip.

```python

pip install happytransformer

from happytransformer import HappyTextToText, TTSettings

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

args = TTSettings(num_beams=5, min_length=1)

# Add the prefix "grammar: " before each input 
result = happy_tt.generate_text("grammar: This sentences has has bads grammar.", args=args)

print(result.text) # Output: "This sentence has bad grammar."

```