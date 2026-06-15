import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import uuid

# Use better model (base is weak)
model = whisper.load_model("small")

def record_audio(duration=8, samplerate=16000):
    print("Recording... Speak clearly")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"   # correct format for wav
    )
    sd.wait()

    filename = f"temp_{uuid.uuid4().hex}.wav"

    # normalize safely
    audio = np.squeeze(audio)
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))
        audio = (audio * 32767).astype(np.int16)

    wav.write(filename, samplerate, audio)

    print("Saved file:", filename)

    return filename


def transcribe_audio(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # First pass: auto detect
    result = model.transcribe(
        file_path,
        fp16=False,
        task="transcribe"
    )

    text = result["text"].strip()
    lang = result["language"]

    print("Detected language:", lang)

    # fallback if garbage / too short
    if len(text) < 5:
        print("Low confidence. Retrying with English...")
        result = model.transcribe(
            file_path,
            fp16=False,
            language="en"
        )
        text = result["text"].strip()

    return text