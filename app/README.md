# 📡 Real-Time Phrases Desktop App

This is a **real-time desktop application** built with **Python + PyQt6** that connects to a WebSocket server and displays incoming phrases in real time.

## 🚀 Features

- Native desktop UI using PyQt6
- WebSocket client for real-time updates
- Displays incoming phrases/messages in a scrollable text area
- Automatically appends new messages as they arrive
- Thread-safe communication between WebSocket and UI

---

## 🖼️ Preview

![app-screenshot](docs/screenshot.png) *(optional)*

---

## 🛠️ Tech Stack

| Layer    | Tool             |
|----------|------------------|
| UI       | PyQt6            |
| Real-Time | `websocket-client` |
| Threading | PyQt Signals / QThread |