from __future__ import annotations

import argparse
import re
import threading
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from TTS.api import TTS

try:
    import gradio as gr
except Exception:
    gr = None


MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
DEFAULT_SPEAKER = "Chandra MacFarland"
AUTO_SPEAKER = "Auto (varsayilan)"
MAX_CHARS = 220
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

_torch_load = torch.load


def _patched_torch_load(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _torch_load(*args, **kwargs)


torch.load = _patched_torch_load


def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    text = " ".join((text or "").split())
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    current = ""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if not sentence:
            continue
        candidate = f"{current} {sentence}".strip()
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
        current = ""
        for word in sentence.split():
            candidate = f"{current} {word}".strip()
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                current = word
    if current:
        chunks.append(current)
    return chunks


def _write_chunk(tts: TTS, text: str, file_path: Path, speaker: str | None, speed: float) -> None:
    kwargs = {
        "text": text,
        "language": "tr",
        "file_path": str(file_path),
        "speed": speed,
        "split_sentences": False,
    }
    if speaker:
        kwargs["speaker"] = speaker
    tts.tts_to_file(**kwargs)


def _extract_speakers_from_model(tts: TTS) -> list[str]:
    names: list[str] = []

    raw_speakers = getattr(tts, "speakers", None)
    if isinstance(raw_speakers, dict):
        names.extend(str(k) for k in raw_speakers.keys())
    elif isinstance(raw_speakers, (list, tuple, set)):
        names.extend(str(x) for x in raw_speakers)
    elif raw_speakers is not None and not isinstance(raw_speakers, str):
        try:
            names.extend(str(x) for x in raw_speakers)
        except TypeError:
            pass

    tts_model = getattr(getattr(tts, "synthesizer", None), "tts_model", None)
    speaker_manager = getattr(tts_model, "speaker_manager", None)
    if speaker_manager is not None:
        manager_speakers = getattr(speaker_manager, "speakers", None)
        if isinstance(manager_speakers, dict):
            names.extend(str(k) for k in manager_speakers.keys())
        elif isinstance(manager_speakers, (list, tuple, set)):
            names.extend(str(x) for x in manager_speakers)

        name_to_id = getattr(speaker_manager, "name_to_id", None)
        if isinstance(name_to_id, dict):
            names.extend(str(k) for k in name_to_id.keys())
        elif name_to_id is not None and not isinstance(name_to_id, str):
            try:
                names.extend(str(x) for x in name_to_id)
            except TypeError:
                pass

    unique_names: list[str] = []
    seen = set()
    for name in names:
        clean = (name or "").strip()
        if clean and clean not in seen:
            seen.add(clean)
            unique_names.append(clean)
    return unique_names


class LocalXTTS:
    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts: TTS | None = None
        self.lock = threading.Lock()

    def _load_model(self) -> TTS:
        if self.tts is None:
            self.tts = TTS(model_name=MODEL_NAME).to(self.device)
        return self.tts

    def list_speakers(self) -> list[str]:
        with self.lock:
            tts = self._load_model()
            return _extract_speakers_from_model(tts)

    def _resolve_speaker(self, tts: TTS, requested: str | None) -> str | None:
        speakers = _extract_speakers_from_model(tts)
        if requested and requested != AUTO_SPEAKER:
            if speakers and requested not in speakers:
                raise ValueError(f"Speaker bulunamadi: {requested}")
            return requested
        if speakers:
            if DEFAULT_SPEAKER in speakers:
                return DEFAULT_SPEAKER
            return speakers[0]
        return DEFAULT_SPEAKER

    def generate(self, text: str, speed: float, speaker_choice: str | None) -> tuple[Path, str | None, int]:
        clean_text = " ".join((text or "").split())
        if not clean_text:
            raise ValueError("Bos metin verildi.")

        with self.lock:
            tts = self._load_model()
            speaker = self._resolve_speaker(tts, speaker_choice)
            parts = split_text(clean_text)
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            out_file = OUTPUT_DIR / f"output_{int(time.time() * 1000)}.wav"

            if len(parts) == 1:
                _write_chunk(tts, parts[0], out_file, speaker, speed)
                return out_file, speaker, 1

            all_audio = []
            sample_rate = None
            for i, part in enumerate(parts, start=1):
                temp_file = OUTPUT_DIR / f"_part_{i}_{int(time.time() * 1000)}.wav"
                _write_chunk(tts, part, temp_file, speaker, speed)
                audio, sr = sf.read(temp_file)
                temp_file.unlink(missing_ok=True)
                if sample_rate is None:
                    sample_rate = sr
                all_audio.append(audio)
                if i < len(parts):
                    gap_len = int(sr * 0.12)
                    if audio.ndim == 1:
                        all_audio.append(np.zeros(gap_len, dtype=audio.dtype))
                    else:
                        all_audio.append(np.zeros((gap_len, audio.shape[1]), dtype=audio.dtype))

            sf.write(out_file, np.concatenate(all_audio), sample_rate)
            return out_file, speaker, len(parts)


def build_gradio_app(service: LocalXTTS) -> "gr.Blocks":
    initial_speakers = [AUTO_SPEAKER]
    initial_status = ""
    try:
        speakers = service.list_speakers()
        if speakers:
            initial_speakers = [AUTO_SPEAKER, *speakers]
            initial_status = f"{len(speakers)} speaker yuklendi."
    except Exception as exc:
        initial_status = f"Speaker listesi yuklenemedi: {exc}"

    with gr.Blocks(title="Coqui XTTS v2 - Turkce TTS") as demo:
        gr.Markdown("## Coqui XTTS v2 - Turkce Ses Uretici (Local)")
        gr.Markdown("Metni yaz, `Ses Uret` butonuna bas. Dosya `output/` klasorune kaydedilir.")

        text_input = gr.Textbox(label="Metin", lines=8, placeholder="Turkce metni buraya yazin...")
        with gr.Row():
            speed_input = gr.Slider(minimum=0.7, maximum=1.6, value=1.2, step=0.05, label="Hiz")
            speaker_input = gr.Dropdown(
                choices=initial_speakers,
                value=AUTO_SPEAKER,
                label="Speaker",
                allow_custom_value=False,
            )
        with gr.Row():
            generate_btn = gr.Button("Ses Uret", variant="primary")
            load_speakers_btn = gr.Button("Speakerlari Yenile")
            clear_btn = gr.Button("Temizle")

        audio_output = gr.Audio(label="Uretilen Ses", type="filepath")
        status_output = gr.Textbox(label="Durum", value=initial_status, interactive=False)

        def ui_generate(text: str, speed: float, speaker: str):
            try:
                out_file, selected_speaker, piece_count = service.generate(text, speed, speaker)
                status = (
                    f"Kaydedildi: {out_file}\n"
                    f"Speaker: {selected_speaker}\n"
                    f"Parca sayisi: {piece_count}"
                )
                return str(out_file), status
            except Exception as exc:
                return None, f"Hata: {exc}"

        def ui_load_speakers():
            try:
                speakers = service.list_speakers()
                if not speakers:
                    return gr.update(choices=[AUTO_SPEAKER], value=AUTO_SPEAKER), "Speaker listesi bulunamadi."
                return (
                    gr.update(choices=[AUTO_SPEAKER, *speakers], value=AUTO_SPEAKER),
                    f"{len(speakers)} speaker bulundu.",
                )
            except Exception as exc:
                return gr.update(choices=[AUTO_SPEAKER], value=AUTO_SPEAKER), f"Hata: {exc}"

        def ui_clear():
            return "", None, ""

        generate_btn.click(
            ui_generate,
            inputs=[text_input, speed_input, speaker_input],
            outputs=[audio_output, status_output],
        )
        load_speakers_btn.click(
            ui_load_speakers,
            inputs=[],
            outputs=[speaker_input, status_output],
        )
        clear_btn.click(
            ui_clear,
            inputs=[],
            outputs=[text_input, audio_output, status_output],
        )

    return demo


def run_cli(service: LocalXTTS, speed: float, speaker: str | None) -> None:
    print("Metni yazip Enter'a basin. Cikis icin: q")
    while True:
        try:
            text = input("Metin: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCikis yapildi.")
            return
        if text.lower() in {"q", "quit", "exit"}:
            print("Cikis yapildi.")
            return
        if not text:
            continue
        out_file, selected_speaker, piece_count = service.generate(text, speed, speaker)
        print(f"Kaydedildi: {out_file} | Speaker: {selected_speaker} | Parca: {piece_count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local Coqui XTTS v2 Turkish TTS")
    parser.add_argument("--mode", choices=["gradio", "cli"], default="gradio")
    parser.add_argument("--host", default="127.0.0.1", help="Gradio host")
    parser.add_argument("--port", type=int, default=7860, help="Gradio port")
    parser.add_argument("--share", action="store_true", help="Enable gradio share link")
    parser.add_argument("--speed", type=float, default=1.2, help="Speech speed")
    parser.add_argument("--speaker", help="Optional speaker name")
    args = parser.parse_args()

    service = LocalXTTS()

    if args.mode == "cli":
        run_cli(service, args.speed, args.speaker)
        return

    if gr is None:
        raise SystemExit("gradio kurulu degil. Kurulum: pip install gradio")

    demo = build_gradio_app(service)
    demo.queue(default_concurrency_limit=1).launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        inbrowser=True,
    )


if __name__ == "__main__":
    main()
