import datetime
import os
import pyperclip
from os.path import exists
from PyUtils.SkyAudioEncoder import SkyAudioEncoder
from PyUtils.MusicUtils import MusicUtils
from PyUtils.FileUtils import FileUtils
from PyUtils.FileUtils import Exts
from Gui.AudioData import AudioData



class AudioLogicLayer:

    def __init__(self, audio_encoders_dir, ):
        self.encoder = SkyAudioEncoder(audio_encoders_dir)
        self.player = MusicUtils()

    def generate_list_audio_data(self):
        """
        Generates the list of audio data used to fill the AudioWindow table.
        :return:
        """
        list_audio_data = []
        skyrim_path = self.app.settings_obj.skyrim_path
        comments_csv = self.app.settings_obj.comments_file
        actors_csv = self.app.settings_obj.actors_file
        scene_order_csv = self.app.settings_obj.scene_order_file
        docs_dir = self.app.settings_obj.docgen_dir
        # todo
        return list_audio_data

    def play_sound(self, sound_path: str):
        """
        Screen Element: Play Button
        :param sound_path:
        :return:
        """
        ret = self._generate_wav_if_not_exit(sound_path)
        if ret:
            wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
            self.player.play(wav_file)
        else:
            print("todo: show message box")

    def play_info(self):
        """
        Screen Element: song progress bar.
        Used to update the screen with the song information in realtime.
        :return: Return a list with the data of the track being played.
        """
        is_playing = self.player.is_playing()
        volume = int(self.player.get_volume() * 100)
        position = str(datetime.timedelta(seconds=self.player.position()))
        sound_len = str(datetime.timedelta(seconds=self.player.len()))
        track = self.player.get_track()
        return [is_playing, volume, position, sound_len, track]

    def set_volume(self, volume: int):
        """
        Screen Element: Volume bar.
        :param volume:
        :return:
        """
        v_in = volume/100
        self.player.set_volume(v_in)

    def open_folder(self, sound_path: str):
        """
        Screen Element: Open Folder Button
        :param sound_path:
        :return:
        """
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        fuz_file = FileUtils.change_ext(sound_path, Exts.EXT_FUZ)
        if exists(wav_file):
            FileUtils.open_file_on_file_explorer(wav_file)
            return True
        if exists(xwm_file):
            FileUtils.open_file_on_file_explorer(xwm_file)
            return True
        if exists(fuz_file):
            FileUtils.open_file_on_file_explorer(fuz_file)
            return True
        return False

    def copy_track_name(self, sound_path: str):
        pyperclip.copy(sound_path)
        return True

    def copy_track_info(self, sound_path: str, list_audio_data):
        data: AudioData
        out_data = ""
        for data in list_audio_data:
            if data.file_path == sound_path:
                out_data = data.to_string()
        pyperclip.copy(out_data)
        if out_data == "":
            return False
        else:
            return True

    def audio_gen_xwm(self, sound_path: str):
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        # garante que o WAV exista, para que XWM possa ser gerado
        if not self._generate_wav_if_not_exit(sound_path):
            print("Wav não pode ser gerado, tente UnFuz")
            return False
        # criar XWM, pergunte caso arquivo ja exista
        resp = False
        if exists(xwm_file):
            print("Deseja continuar?")
            if resp:
                self.encoder.wav_to_xwm(sound_path)
            else:
                print("Geração cancelada")
        else:
            self.encoder.wav_to_xwm(sound_path)

    def audio_gen_fuz(self, sound_path: str):
        fuz_file = FileUtils.change_ext(sound_path, Exts.EXT_FUZ)
        return self.encoder.fuz(sound_path)

    def audio_unfuz(self, sound_path: str):
        lip_file = FileUtils.change_ext(sound_path, Exts.EXT_LIP)
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        exit_file = []
        resp = True
        if exists(wav_file):
            exit_file.append(wav_file)
        if exists(xwm_file):
            exit_file.append(xwm_file)
        if exists(lip_file):
            exit_file.append(lip_file)
        if len(exit_file) > 0:
            print("Os seguintes arquivos serão sobreescritos. " + str(exit_file) + ". Deseja continuar?")
            resp = True
        if resp == True:
            return self.encoder.unfuz(sound_path)
        return resp

    def _generate_wav_if_not_exit(self, sound_path):
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        if not exists(wav_file):
            if exists(xwm_file):
                self.encoder.xwm_to_wav(sound_path)
            else:
                print("Arquivo wav não existe, XWM não pode ser gerado. Tente usar UnFuz.")
                return False
        return True