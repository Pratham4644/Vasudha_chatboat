import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.speech_to_text import record_audio, transcribe_audio

if __name__ == "__main__":
    file = record_audio(8)
    text = transcribe_audio(file)

    print("\nTRANSCRIPTION:")
    print(text)