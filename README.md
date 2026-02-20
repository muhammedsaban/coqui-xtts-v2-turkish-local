# Coqui XTTS v2 Turkish TTS (Local-First)

Production-ready, local web arayuzu ile Turkce metni hizli sekilde sese ceviren Coqui XTTS v2 uygulamasi.

Bu proje sunucu gerektirmez. Kullanici uygulamayi kendi bilgisayarinda calistirir, ses dosyalari yerel olarak uretilir.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
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

Bu repo, Turkce icerik ureticileri icin pratik bir text-to-speech (TTS) akisi sunar:

1. Metni gir.
2. Speaker sec.
3. Hizi ayarla.
4. Tek tikla WAV dosyasini al.

Arayuz `localhost` uzerinde calisir. Cikti dosyalari `output/` klasorune yazilir.

## Key Features

- Coqui XTTS v2 tabanli Turkce TTS
- Local Gradio UI (`http://127.0.0.1:7860`)
- Modelden otomatik speaker listesi cekme
- Speed kontrolu
- Uzun metinlerde otomatik parcala + birlestir
- CLI destegi
- Local-first mimari (sunucu masrafi yok)

## System Requirements

- OS: Windows 10/11
- Python: `3.10` veya `3.11`
- RAM: minimum 8 GB onerilir
- GPU: opsiyonel (CUDA varsa daha hizli)
- Internet: ilk model indirmesi icin gerekli

## Quick Start

### 1) Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2) Run web app

```powershell
.\start_gradio.bat
```

Alternatif:

```powershell
python app.py --mode gradio
```

### 3) Open UI

Tarayici adresi:

`http://127.0.0.1:7860`

## Usage

1. `Metin` alanina Turkce metni gir.
2. `Speaker` dropdown'undan sesi sec.
3. `Hiz` slider'i ile konusma hizini ayarla.
4. `Ses Uret` butonuna tikla.
5. Uretilen sesi dinle veya dosya olarak kullan.

## CLI Mode

Interactive terminal modu:

```powershell
python app.py --mode cli
```

Cikis komutlari: `q`, `quit`, `exit`

## Configuration

Temel parametreler:

- `--mode {gradio,cli}`: Calisma modu
- `--host`: Gradio host (default: `127.0.0.1`)
- `--port`: Gradio port (default: `7860`)
- `--speed`: Konusma hizi (default: `1.2`)
- `--speaker`: Secili speaker adi
- `--share`: Gecici public Gradio linki olusturur

Ornek:

```powershell
python app.py --mode gradio --host 127.0.0.1 --port 7860
```

## Output

- Tum ses dosyalari: `output/`
- Format: `.wav`
- Uzun metinlerde tek dosya olarak birlestirilmis sonuc uretir

## Troubleshooting

### `gradio kurulu degil` hatasi

```powershell
python -m pip install -r requirements.txt
```

### Ilk acilista yavaslik

Model ilk kez indirildigi icin normaldir. Sonraki calistirmalar daha hizli olur.

### Speaker listesi bos gorunuyor

- `Speakerlari Yenile` butonunu kullan.
- Internet baglantisini ve model indirmesini kontrol et.
- Uygulamayi yeniden baslat.

### CPU'da yavas calisma

GPU zorunlu degil ancak hiz icin CUDA destekli NVIDIA GPU onerilir.

## Privacy

- Metin ve ses dosyalari yerel calisir.
- Varsayilan akista harici bir API'ye veri gonderilmez.
- Uretilen ses dosyalari sadece sizin makinenizdeki `output/` klasorune yazilir.

## License

Bu projenin kodu `MIT` lisansi altinda dagitilir. Detay:

`LICENSE`

Not: Coqui TTS kutuphanesi ve XTTS model lisanslari ayri kapsamda degerlendirilmelidir. Ticari kullanimdan once ilgili lisanslari ayrica kontrol edin.
