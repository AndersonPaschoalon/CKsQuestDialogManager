import datetime
import os
import PySimpleGUI as sg
import pyperclip
from os.path import exists
from PyUtils.SkyAudioEncoder import SkyAudioEncoder
from PyUtils.MusicUtils import MusicUtils
from PyUtils.FileUtils import FileUtils
from PyUtils.FileUtils import Exts
from Gui.AudioData import AudioData
from PyUtils.Logger import Logger
from Gui.AppInfo import AppInfo
from PyUtils.Obj2Json import Obj2Json
from QuestExports.QuestDialogs import QuestDialogs
from QuestExports.Scene import Scene
from QuestExports.SceneTopic import SceneTopic
from QuestExports.BranchDialogs import BranchDialogs
from QuestExports.TopicDialogs import TopicDialogs


class AudioLogicLayer:

    STR_INFO_POPUP = "Info"
    STR_ERROR_POPUP = "Error"

    def __init__(self, app_dir):
        self.app = AppInfo(app_dir)
        self._log = Logger.get()
        self.encoder = SkyAudioEncoder(self.app.audio_encoder_dir)
        self.player = MusicUtils()

    def generate_list_audio_data(self):
        """
        Generates the list of audio data used to fill the AudioWindow table.
        :return:
        """
        self._log.debug("-- generate_list_audio_data()")
        skyrim_path = self.app.settings_obj.skyrim_path
        comments_csv = self.app.settings_obj.comments_file
        actors_csv = self.app.settings_obj.actors_file
        scene_order_csv = self.app.settings_obj.scene_order_file
        list_audio_data = AudioData.generate_list_audio_data(skyrim_path, comments_csv, actors_csv, scene_order_csv)
        return list_audio_data

    def play_sound(self, sound_path: str):
        """
        Screen Element: Play Button
        :param sound_path:
        :return:
        """
        self._log.debug("-- play_sound() sound_path:" + sound_path)
        if sound_path == "":
            popup_text = "No sound file selected."
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)
            return
        ret_val = self.encoder.try_to_gen_wav(sound_path, force_generation=False)
        if ret_val == SkyAudioEncoder.RET_SUCCESS:
            wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
            self.player.play(wav_file)
        else:
            ret_msg = self.encoder.get_last_error()
            err_description = self.encoder.get_last_stdout()
            popup_text = "Error playing track " + sound_path + ": " + ret_msg + "\n\n" + err_description
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title="Play Audio Error")

    def stop_sound(self):
        """
        Screen Element: Stop Button
        :return:
        """
        self._log.debug("-- stop_sound()")
        self.player.stop()

    def pause_sound(self):
        """
        Screen Element: Pause Button
        :return:
        """
        self._log.debug("-- stop_sound()")
        self.player.pause()

    def play_info(self):
        """
        Screen Element: song progress bar.
        Used to update the screen with the song information in realtime.
        :return: Return a list with the data of the track being played.
        """
        self._log.debug("-- play_info()")
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
        self._log.debug("-- set_volume() " + str(volume))
        v_in = volume/100
        self.player.set_volume(v_in)

    def open_folder(self, sound_path: str):
        """
        Screen Element: Open Folder Button
        :param sound_path:
        :return:
        """
        self._log.debug("-- open_folder()")
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        fuz_file = FileUtils.change_ext(sound_path, Exts.EXT_FUZ)
        if exists(wav_file):
            FileUtils.open_file_on_file_explorer(wav_file)
            return
        if exists(xwm_file):
            FileUtils.open_file_on_file_explorer(xwm_file)
            return
        if exists(fuz_file):
            FileUtils.open_file_on_file_explorer(fuz_file)
            return
        popup_text = "File " + sound_path + " not found."
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)

    def copy_track_name(self, sound_path: str):
        """
        Copy the track name to the clipboard.
        :param sound_path:
        :return:
        """
        self._log.debug("-- copy_track_name()")
        pyperclip.copy(sound_path)
        popup_text = "Track name " + sound_path + " was copied to the clipboard."
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)

    def copy_track_info(self, sound_path: str, list_audio_data):
        """
        Copy track info to clipboard.
        :param sound_path:
        :param list_audio_data:
        """
        self._log.debug("-- copy_track_info()")
        data: AudioData
        out_data = ""
        for data in list_audio_data:
            if data.file_path == sound_path:
                out_data = data.to_string()
        pyperclip.copy(out_data)
        popup_text = "Track information as copied to the clipboard: \n" + out_data
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)

    def audio_gen_xwm(self, sound_path: str):
        """
        Generate XWM file.
        :param sound_path:
        """
        self._log.cebug("-- audio_gen_xwm()")
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        # garante que o WAV exista, para que XWM possa ser gerado
        [ret_val, ret_msg] = self._generate_wav_if_not_exit(sound_path)
        if not ret_val:
            popup_text = "Error Generating XWM file " + sound_path + ": " + ret_msg
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            return
        # criar XWM, pergunte caso arquivo ja exista
        if exists(xwm_file):
            popup_text = "The following file is going to be overwritten: \n" + str(xwm_file) +\
                         "\n\nDo you want to continue?"
            popup_ret = sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                                 title=AudioLogicLayer.STR_INFO_POPUP)
            if popup_ret == AudioLogicLayer.STR_CANCEL:
                return
            ret_val = self.encoder.wav_to_xwm(sound_path)
            if not ret_val:
                popup_text = "Error creating XWM file from " + sound_path + ".\nError Message: " +\
                             self.encoder.get_last_error()
                sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                         title=AudioLogicLayer.STR_ERROR_POPUP)
        else:
            ret_val = self.encoder.wav_to_xwm(sound_path)
        if ret_val:
            popup_ret = "Success generating XWM file."
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            return
        else:
            popup_ret = "Error: " +  self.encoder.get_last_error()
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)

    def audio_gen_fuz(self, sound_path: str):
        """
        Generate fuz file.
        :param sound_path:
        :return:
        """
        self._log.cebug("-- audio_gen_fuz()")
        fuz_file = FileUtils.change_ext(sound_path, Exts.EXT_FUZ)
        ret_val = self.encoder.fuz(sound_path)
        if not ret_val:
            popup_text = "Error encoding file into FUZ format: " + self.encoder.get_last_error()
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)

    def audio_unfuz(self, sound_path: str):
        """
        Decode FUZ file into lip, xwm an wav format.
        :param sound_path: sound file.
        """
        self._log.cebug("-- audio_unfuz()")
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
            popup_text = "The following files are going to be overwritten: \n" + str(exit_file) +\
                         "\n\nDo you want to continue?"
            popup_ret = sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)
            if popup_ret == AudioLogicLayer.STR_CANCEL:
                return
        ret_val = self.encoder.unfuz(sound_path)
        if not ret_val:
            popup_text = "Error deconding file " + sound_path + ". Error message:" + self.encoder.get_last_error()
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)

    def get_current_track_len(self):
        """
        Returns track len in seconds.
        :return:
        """
        return self.player.len()

    def get_current_track_progress(self):
        """
        Returns track progress in seconds.
        :return:
        """
        return self.player.position()

    def _generate_wav_if_not_exit(self, sound_path):
        """
        Try to generate WAV file if it does not exit.
        :param sound_path: Path of the file to be used on the generation of the wav file.
        :return: return a vector [ret_val: bool, ret_msg: str], where ret_val is True if the WAV file already exits,
        or it was rightly generated. Returns False in case some error ocurred generating the WAV file. In case ret_val
        id True ret_msg will be an empty sttring. Otherwise it will contains the Error message.
        """
        self._log.debug("-- _generate_wav_if_not_exit()")
        ret_val = False
        ret_msg = ""
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        mp3_file = FileUtils.change_ext(sound_path, Exts.EXT_MP3)
        self._log.debug("wav_file:" + wav_file + ", xwm_file:" + xwm_file + ", mp3_file:" + mp3_file)
        if not exists(wav_file):
            self._log.info("WAV file for <" + sound_path + "> was not found. Search for alternatives: XWM and MP3...")
            # try to generate file from XWM
            if exists(xwm_file):
                self._log.info("XWM was found for " + sound_path)
                ret_val = self.encoder.xwm_to_wav(sound_path)
                if not ret_val:
                    ret_msg = self.encoder.get_last_error()
                    self._log.error("Last error: " + self.encoder.get_last_error())
                    self._log.error("Last stdout: " + self.encoder.get_last_stdout())
            # try mp3 format
            elif exists(mp3_file):
                self._log.info("MP3 was found for " + sound_path)
                ret_val = self.encoder.mp3_to_wav(sound_path)
                if not ret_val:
                    ret_msg = self.encoder.get_last_error()
                    self._log.error("Last error: " + self.encoder.get_last_error())
                    self._log.error("Last stdout: " + self.encoder.get_last_stdout())
            else:
                ret_msg = "WAV file does not exit for track \"" + sound_path + \
                          "\", and no alternative (xwm or mp3) was found.\n Try to use UnFuz first."
                self._log.error("ret_msg:" + ret_msg)
        else:
            ret_val = True
        self._log.debug(str([ret_val, ret_msg]))
        return [ret_val, ret_msg]

