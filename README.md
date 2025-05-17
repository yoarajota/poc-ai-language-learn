# Speech Pronunciation Correction Desktop App

A **real-time desktop application** built with **Python + PyQt6** that corrects speech pronunciation by processing live audio, transcribing it into text, refining it with a Large Language Model (LLM), comparing phonetic representations, and providing auditory feedback via Text-to-Speech (TTS). The app connects to a WebSocket server to display incoming phrases in real time.

## CURRENT TRYED APPROACH
### Conclusion: this approach is not optimal/functional.

## 🚀 Features

- **Real-Time Speech Processing**: Captures live audio, segments it into phrases, and transcribes using Speech-to-Text (STT).
- **Pronunciation Correction**: Refines transcribed phrases with an LLM and compares phonetic representations (G2P) to identify errors.
- **Auditory Feedback**: Uses TTS to play corrected pronunciations for user learning.
- **Native Desktop UI**: Built with PyQt6, featuring a scrollable text area for displaying incoming and corrected phrases.
- **WebSocket Integration**: Connects to a WebSocket server for real-time phrase updates.
- **Thread-Safe Communication**: Ensures smooth interaction between WebSocket, UI, and processing threads using PyQt Signals and QThread.
- **Iterative Learning**: Allows users to repeat phrases and refine pronunciation through feedback loops.

---

## 🛠️ Tech Stack

| Layer              | Tool                              |
|--------------------|-----------------------------------|
| UI                 | PyQt6                            |
| Real-Time          | `websocket-client`               |
| Threading          | PyQt Signals / QThread           |
| Speech-to-Text     | OpenAI Whisper (or similar)      |
| Language Model     | LLM API (e.g., GPT-based model)  |
| Grapheme-to-Phoneme| NVIDIA NeMo G2P / g2p_seq2seq    |
| Text-to-Speech     | NVIDIA NeMo TTS (or similar)     |
| Audio Processing   | `pyaudio` / `sounddevice`        |

---

## 📋 System Roadmap

The application follows a structured pipeline to correct pronunciation:

1. **Stream Speech to Text in Phrases**:
   - Captures live audio using `pyaudio` or `sounddevice`.
   - Uses Voice Activity Detection (VAD) to segment audio into meaningful phrases.
   - Transcribes phrases in real time with a Speech-to-Text system (e.g., OpenAI Whisper).

2. **Send Text to LLM to Fix Phrases**:
   - Sends transcribed phrases to an LLM via API or integrated model.
   - Uses tailored prompts to correct pronunciation or phrasing errors.
   - Stores corrected text for further processing.

3. **Transform Both Texts into G2P Responses**:
   - Converts original and corrected texts into phonetic sequences using a Grapheme-to-Phoneme (G2P) model (e.g., NVIDIA NeMo G2P or CiscoDevNet `g2p_seq2seq_pytorch`).
   - Generates phonetic transcriptions for comparison.

4. **Compare G2P Responses**:
   - Compares phonetic sequences using algorithms like edit distance or similarity metrics.
   - Identifies discrepancies to confirm if pronunciation issues persist.

5. **Use TTS to Help Fix Pronunciation**:
   - Generates audio of corrected text using a TTS engine (e.g., NVIDIA NeMo TTS).
   - Plays audio to guide users on correct pronunciation.
   - Optionally prompts users to repeat phrases, restarting the pipeline for refinement.

---

## 🛠️ Installation

### Prerequisites
- Python 3.12+
- PyQt6
- `websocket-client`
- `pyaudio` or `sounddevice`
- Speech-to-Text model (e.g., OpenAI Whisper)
- G2P model (e.g., NVIDIA NeMo or `g2p_seq2seq_pytorch`)
- TTS engine (e.g., NVIDIA NeMo TTS)
- LLM access (e.g., API key for GPT-based model)

---

## 📖 Usage

1. Launch the app to open the PyQt6 interface.
2. Speak into your microphone; the app will transcribe phrases in real time.
3. View original and corrected phrases in the scrollable text area.
4. If pronunciation errors are detected, listen to the TTS-generated audio for guidance.
5. Repeat phrases as prompted to improve pronunciation.

---

## 📚 References

- **Speech-to-Text**:
  - [OpenAI Whisper GitHub Repository](https://github.com/openai/whisper)
- **G2P Models**:
  - [NVIDIA NeMo Toolkit G2P Documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tts/g2p.html)
  - [CiscoDevNet g2p_seq2seq_pytorch Example](https://github.com/CiscoDevNet/g2p_seq2seq_pytorch)
- **Text-to-Speech**:
  - [NVIDIA NeMo TTS Documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tts/overview.html)
- **Pronunciation Correction**:
  - [ArXiv: Fixing Pronunciation in LLMs](https://arxiv.org/html/2404.02456v1)
- **PyQt6**:
  - [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- **WebSocket**:
  - [websocket-client GitHub Repository](https://github.com/websocket-client/websocket-client)

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## 📜 License

This project is licensed under the MIT License.
