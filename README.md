# 📡 Real-Time Phrases Desktop App

A **real-time desktop application** built with **Python + PyQt6** that connects to a WebSocket server and displays incoming phrases in real time. This app is part of a broader **Speech Pronunciation Correction System** designed to capture, process, and correct speech pronunciations using advanced technologies.

## 🚀 Features

- **Native Desktop UI**: Built with PyQt6 for a responsive and intuitive user interface.
- **Real-Time Updates**: WebSocket client for seamless, real-time phrase updates.
- **Scrollable Text Area**: Displays incoming phrases/messages with automatic appending.
- **Thread-Safe**: Ensures safe communication between WebSocket and UI using PyQt Signals and QThread.

## 🛠️ Tech Stack

| Layer | Tool |
| --- | --- |
| UI | PyQt6 |
| Real-Time | `websocket-client` |
| Threading | PyQt Signals / QThread |

## 🎯 Speech Pronunciation Correction System Roadmap

This application is a component of a larger system aimed at correcting speech pronunciations. Below is the roadmap for the complete system:

1. **Stream Speech to Text in Phrases**

   - Capture live audio and segment it into phrases using real-time audio processing libraries (`pyaudio` or `sounddevice`).
   - Use Voice Activity Detection (VAD) to identify phrase boundaries.
   - Transcribe each phrase individually.

2. **Send Text to LLM to Fix Phrases**

   - Process transcribed phrases with a Large Language Model (LLM) to correct errors.
   - Send phrases to an LLM via API or integrated model with prompts targeting pronunciation issues.
   - Store the corrected text.

3. **Transform Both Texts into G2P Responses**

   - Convert original and corrected texts into phonetic representations using a Grapheme-to-Phoneme (G2P) model (e.g., NVIDIA NeMo Toolkit G2P or CiscoDevNet `g2p_seq2seq_pytorch`).
   - Generate phoneme sequences for both texts.

4. **Compare G2P Responses**

   - Compare phonetic representations using algorithms like edit distance or similarity metrics.
   - Identify discrepancies indicating unresolved pronunciation errors.

5. **Use TTS to Help Fix Pronunciation**

   - Provide auditory feedback using a Text-to-Speech (TTS) engine (e.g., NVIDIA NeMo TTS).
   - Play synthesized audio of the corrected text to guide users.
   - Optionally, prompt users to repeat and re-run the pipeline for refinement.

## 📚 References

- **Fixing Pronunciation in LLMs**: ArXiv: Fixing Pronunciation in LLMs
- **G2P Models**:
  - NVIDIA NeMo Toolkit G2P Documentation
  - CiscoDevNet g2p_seq2seq_pytorch Example
- **Speech-to-Text**: OpenAI Whisper GitHub Repository
