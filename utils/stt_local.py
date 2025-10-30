import speech_recognition as sr
import time
from utils.audio_capture import Recorder
from config import SILENCE_THRESHOLD

def listen_and_transcribe():
    """
    Menerapkan Voice Activity Detection (VAD) sederhana.
    Mendengarkan hingga ada suara, merekam hingga kembali hening, lalu transkripsi.
    """
    recorder = Recorder()
    r = sr.Recognizer()

    if not recorder.start():
        return None

    print("[🎧] Menunggu suara Luna...")

    # 1. Tunggu hingga ada suara
    while True:
        chunk = recorder.record_chunk()
        if not recorder.is_silent(chunk):
            print("[🗣️] Suara terdeteksi, mulai merekam...")
            break

    # 2. Rekam hingga kembali hening
    frames = [chunk] # Sertakan chunk pertama yang bersuara
    silent_chunks = 0
    max_silent_chunks = int(SILENCE_THRESHOLD * (recorder.RATE / recorder.CHUNK))

    while silent_chunks < max_silent_chunks:
        chunk = recorder.record_chunk()
        frames.append(chunk)
        if recorder.is_silent(chunk):
            silent_chunks += 1
        else:
            silent_chunks = 0 # Reset jika ada suara lagi

    print(f"[🕓] Hening terdeteksi selama {SILENCE_THRESHOLD} detik, berhenti merekam.")
    recorder.stop()

    # 3. Transkripsi seluruh rekaman
    hasil_final = ""
    if frames:
        wav_data = recorder.convert_frames_to_wav(frames)
        try:
            with sr.AudioFile(wav_data) as source:
                audio = r.record(source)
            hasil_final = r.recognize_google(audio, language="id-ID")
            print(f"[✅] Transkripsi lengkap: {hasil_final}")
        except sr.UnknownValueError:
            print("[⚠️] Tidak ada suara yang bisa dikenali dari rekaman.")
        except sr.RequestError as e:
            print(f"[❌] Error koneksi STT: {e}")

    if not hasil_final:
        print("[⚠️] Tidak ada hasil transkripsi.")

    return hasil_final.strip()
