import pyaudio
import wave
import io
import audioop
from config import AUDIO_ENERGY_THRESHOLD

def find_loopback_device(p):
    """Cari device audio loopback seperti 'Stereo Mix' atau 'CABLE Output'."""
    possible_devices = ["Stereo Mix", "CABLE Output"]
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        for device_name in possible_devices:
            if device_name in info["name"]:
                print(f"[🎤] Ditemukan device loopback: {info['name']}")
                return i
    print(f"[⚠️] Tidak ditemukan device loopback. Pastikan 'Stereo Mix' atau 'VB-Cable' aktif.")
    return None

class Recorder:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.device_index = find_loopback_device(self.p)
        self.stream = None
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100

    def start(self):
        if self.device_index is None:
            print("[❌] Gagal memulai rekaman, perangkat loopback tidak ditemukan.")
            return False

        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK,
                                  input_device_index=self.device_index)
        print("[🔴] Rekaman dimulai.")
        return True

    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        print("[⏹️] Rekaman dihentikan.")

    def record_chunk(self):
        if not self.stream:
            return None
        return self.stream.read(self.CHUNK)

    def is_silent(self, chunk):
        """Cek apakah sebuah chunk audio dianggap hening berdasarkan energinya."""
        if chunk is None:
            return True
        energy = audioop.rms(chunk, 2)  # Root Mean Square
        return energy < AUDIO_ENERGY_THRESHOLD

    def convert_frames_to_wav(self, frames):
        """Mengubah frame audio mentah menjadi format WAV dalam memory."""
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
        wav_buffer.seek(0)
        return wav_buffer
