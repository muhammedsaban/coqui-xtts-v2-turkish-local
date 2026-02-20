![Project Logo](assets/logo.png)

# Coqui XTTS v2 Turkish TTS (Local-First)

**Primary TTS model:** [Coqui XTTS v2](https://docs.coqui.ai/en/latest/models/xtts.html)

A local-first Turkish text-to-speech app built with Coqui XTTS v2 and Gradio.
Run it on your own computer and generate WAV files without managing a backend server.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Recommended Voice](#recommended-voice)
- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [CLI Mode](#cli-mode)
- [Configuration](#configuration)
- [Output](#output)
- [Troubleshooting](#troubleshooting)
- [Privacy](#privacy)
- [License](#license)

## Overview

This project provides a simple workflow for Turkish content creators:

1. Enter text
2. Choose a speaker
3. Adjust speed
4. Generate a WAV file

The UI runs locally on `localhost`, and all outputs are saved to the `output/` folder.

## Key Features

- Turkish TTS powered by Coqui XTTS v2
- Local Gradio UI (`http://127.0.0.1:7860`)
- Automatic speaker list loading from model data
- Speech speed control
- Long text chunking and automatic merge
- Optional CLI mode
- Local-first architecture (no always-on server required)

## Recommended Voice

For consistent Turkish voiceover quality, the recommended speaker is:

- `Chandra MacFarland`

You can select this speaker from the `Speaker` dropdown in the web UI, or set it with:

```powershell
python app.py --mode cli --speaker "Chandra MacFarland"
```

## System Requirements

- OS: Windows 10/11
- Python: `3.10` or `3.11`
- RAM: 8 GB minimum recommended
- GPU: Optional (faster with CUDA-enabled NVIDIA GPU)
- Internet: Required for the first model download

## Quick Start

### 1) Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2) Run the web app

```powershell
.\start_gradio.bat
```

Alternative:

```powershell
python app.py --mode gradio
```

### 3) Open the UI

`http://127.0.0.1:7860`

## Usage

1. Enter your Turkish text in the `Metin` field.
2. Select `Chandra MacFarland` in the `Speaker` dropdown (recommended).
3. Adjust the `Hiz` slider.
4. Click `Ses Uret`.
5. Preview or reuse the generated WAV file.

## CLI Mode

Run interactive terminal mode:

```powershell
python app.py --mode cli
```

Exit commands: `q`, `quit`, `exit`

## Configuration

Main options:

- `--mode {gradio,cli}`: Execution mode
- `--host`: Gradio host (default: `127.0.0.1`)
- `--port`: Gradio port (default: `7860`)
- `--speed`: Speech speed (default: `1.2`)
- `--speaker`: Speaker name
- `--share`: Creates a temporary public Gradio link

Example:

```powershell
python app.py --mode gradio --host 127.0.0.1 --port 7860
```

## Output

- Directory: `output/`
- Format: `.wav`
- Long text is merged into a single final output file

## Troubleshooting

### `gradio not installed` error

```powershell
python -m pip install -r requirements.txt
```

### Slow first startup

Expected behavior. The model is downloaded and initialized on first run.

### Empty speaker list

- Click `Speakerlari Yenile`
- Check internet connection and model download status
- Restart the app

### Slow generation on CPU

GPU is not required, but generation is significantly faster with CUDA.

## Privacy

- Text and audio processing happens locally
- No external API is required in the default workflow
- Output files stay on your machine under `output/`

## License

This repository is released under the `MIT` license.

See: `LICENSE`

Note: Coqui TTS library and XTTS model licensing are separate. Review upstream licenses before commercial use.
