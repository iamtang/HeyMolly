import playsound
import threading
from pydub import AudioSegment
import time
class MusicPlayer:
    def __init__(self, music_path):
        self.music_path = music_path
        self.is_playing = False
        self.thread = None

    def play(self):
        def run():
            self.is_playing = True
            self.start_time = time.time()
            playsound.playsound(self.music_path)
            self.is_playing = False

        self.thread = threading.Thread(target=run)
        self.thread.start()

    def is_finished(self):
        audio = AudioSegment.from_file(self.music_path)
        duration_ms = len(audio) / 1000
        print(duration_ms)
        return time.time() - self.start_time >= duration_ms
        