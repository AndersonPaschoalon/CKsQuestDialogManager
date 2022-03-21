import os
from pygame import mixer
import time

class MusicUtils:

    def __init__(self):
        print("Initializing mixer from pygame")
        mixer.init()
        self.sound = None

    def play(self, sound_path):
        """
        Play song.
        :param sound_path:
        :return:
        """
        self.sound = mixer.Sound(sound_path)
        mixer.music.load(sound_path)
        mixer.music.play()

    def stop(self):
        """
        Stop song.
        :return:
        """
        mixer.music.stop()

    def pause(self):
        """
        Pause song.
        :return:
        """
        mixer.music.pause()

    def unpause(self):
        """
        Unpause song.
        :return:
        """
        mixer.music.unpause()

    def is_playing(self):
        """
        Tells if it is playing.
        :return:
        """
        if mixer.music.get_busy() == True:
            return True
        return False

    def len(self):
        """
        Tells the sound len in seconds
        :return:
        """
        return int(round(self.sound.get_length()))

    def position(self):
        """
        Tells the current position in seconds
        :return:
        """
        return int(round(mixer.music.get_pos() / 1000))

    def get_volume(self):
        """
        Get the volume from 0.0 (min) up to 1.0 (max)
        :return:
        """
        return mixer.music.get_volume()

    def set_volume(self, new_volume):
        """
        Set the volume from 0.0 (min) up to 1.0 (max).
        If value < 0.0, the volume will not be changed
        If value > 1.0, the volume will be set to 1.0
        :param new_volume:
        :return:
        """
        mixer.music.set_volume(new_volume)


if __name__ == "__main__":
    DURATION = 60*10
    player = MusicUtils()
    player.play_sound('../Sandbox/audio/02 - Carry On.mp3')
    sleep_time = 0
    while sleep_time < DURATION:
        print("sleep_time:" + str(sleep_time) + ", player => sound_len/sound_position:" + str(player.sound_len()) + "/"
              + str(player.sound_position()))
        sleep_time += 1
        time.sleep(1)