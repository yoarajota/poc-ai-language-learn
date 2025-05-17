# Speech

## Try n1: gTTS

### Overview
**gTTS (Google Text-to-Speech)** is a Python library and CLI tool that interfaces with Google Translate's text-to-speech API. It allows you to generate spoken MP3 audio from text, save it to a file, manipulate it as a bytestring, or output it directly to stdout.

### Features
- **Customizable sentence tokenizer**:
  - Handles unlimited text lengths while maintaining proper intonation, abbreviations, decimals, and more.
- **Customizable text pre-processors**:
  - Allows for pronunciation corrections and other text adjustments to improve audio quality.

### Usage Examples

#### Installation
Install the library using pip:
```bash
pip install gtts
```

```python

from gtts import gTTS

# Text to convert to speech
text = "Hello, welcome to the world of text-to-speech!"

# Configure language and generate audio
tts = gTTS(text, lang="en")
tts.save("output.mp3")  # Save the audio to an MP3 file

```

```python

from gtts import gTTS
import os

text = "This is an example of text-to-speech conversion."
tts = gTTS(text, lang="en")
tts.save("example.mp3")

# Play the audio (on Unix systems)
os.system("mpg321 example.mp3")

```

### Conclusion
Using gTTS, I cannot use phonemes, only raw text. 