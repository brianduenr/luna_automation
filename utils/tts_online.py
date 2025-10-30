import os
import time
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io

def speak_text(text):
    """
    Text-to-speech bahasa Indonesia menggunakan gTTS dan playback dengan pydub.
    """
    try:
        # Buat audio di memory, bukan file fisik
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang="id")
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Putar audio dari memory menggunakan pydub
        sound = AudioSegment.from_file(mp3_fp, format="mp3")
        play(sound)

        time.sleep(1) # Beri jeda singkat setelah berbicara
    except Exception as e:
        print(f"[❌] Gagal menghasilkan audio: {e}")
