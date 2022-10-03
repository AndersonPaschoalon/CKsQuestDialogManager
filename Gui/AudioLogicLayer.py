import os
import webbrowser
import pyperclip
import multiprocessing
import PySimpleGUI as sg
import traceback
import sys
from os.path import exists
from threading import Thread
from threading import Lock
from random import randint, randrange
from pydub import AudioSegment
from multiprocessing.pool import ThreadPool
from PyUtils.SkyAudioEncoder import SkyAudioEncoder
from PyUtils.MusicUtils import MusicUtils
from PyUtils.FileUtils import FileUtils
from PyUtils.FileUtils import Exts
from PyUtils.Functions import *
from PyUtils.Logger import Logger
from Gui.AudioData import AudioData
from Gui.ReportBatchCmd import ReportBatchCmd
from Gui.ReportAudioDetails import ReportAudioDetails
from Settings.AppInfo import AppInfo


class AudioLogicLayer:

    STR_INFO_POPUP = "Info"
    STR_ERROR_POPUP = "Error"
    STR_CANCEL = "Cancel"
    STR_OK = "Ok"
    batchReportMutex = Lock()

    def __init__(self, app_dir):
        self.app = AppInfo(app_dir)
        self._log = Logger.get()
        self.encoder = SkyAudioEncoder(self.app.audio_encoder_dir)
        self.player = MusicUtils()
        self.console_output = "CK Audio Manager initialized...\n"
        self._console_has_change = True

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

    def create_audio_details_report(self, list_audio_data, ask_popup=True):
        self._log.debug(" -- create_audio_details_report()")
        list_details = []
        item: AudioData
        for item in list_audio_data:
            status_dict = AudioLogicLayer.file_status_dic(item.file_path)
            details = ReportAudioDetails()
            # audio status
            details.mp3 = status_dict["mp3"]
            details.wav = status_dict["wav"]
            details.xwm = status_dict["xwm"]
            details.lip = status_dict["lip"]
            details.fuz = status_dict["fuz"]
            # dialog data
            details.quest_id = item.quest_id
            details.actor = item.actor_name
            details.file = item.file_name
            details.subtitle = item.subtitle
            details.file_path = item.file_path
            details.dialog_type = item.dialog_type
            details.emotion = item.emotion
            details.voice_type = item.voice_type
            details.topic_id = item.topic_id
            details.branch_id = item.branch_id
            details.scene_id = item.scene_id
            details.scene_phase = item.scene_phase
            list_details.append(details)
        file_name = ReportAudioDetails.export_report(list_details, self.app)
        self._log.debug("file_name:" + str(file_name))
        self._log.debug("Report generation finished.")
        self._console_add("Report generation finished.")
        if ask_popup:
            popup_ret = ""
            popup_text = "Report generation finished. Do you want to open it?"
            popup_ret = sg.popup_ok_cancel(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            self._console_add(popup_text)
            url_report = "file:///" + os.path.realpath(file_name)
            # print("url_report:" + url_report)
            # print("popup_ret:" + popup_ret)
            if popup_ret != AudioLogicLayer.STR_CANCEL:
                webbrowser.open(url_report, new=2)


        return file_name

    @staticmethod
    def file_status_dic(sound_path: str):
        """
        Return a dict with the file status.
        :param sound_path:
        :return:
        """
        if sound_path == "":
            return ""
        file_status_dict = {
            "mp3": "missing",
            "wav": "missing",
            "xwm": "missing",
            "lip": "missing",
            "fuz": "missing"
        }
        mp3_file = FileUtils.change_ext(sound_path, Exts.EXT_MP3)
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        lip_file = FileUtils.change_ext(sound_path, Exts.EXT_LIP)
        fuz_file = FileUtils.change_ext(sound_path, Exts.EXT_FUZ)
        msg = ""
        # mp3
        if exists(mp3_file):
            file_status_dict["mp3"] = "ok"
        # wav
        if exists(wav_file):
            file_status_dict["wav"] = "ok"
        # xwm
        if exists(xwm_file):
            file_status_dict["xwm"] = "ok"
        # lip
        if exists(lip_file):
            file_status_dict["lip"] = "ok"
        # fuz
        if exists(fuz_file):
            file_status_dict["fuz"] = "ok"
        return file_status_dict

    @staticmethod
    def file_status(sound_path: str):
        """
        Return a string with the file status.
        :return:
        """
        # print("** sound_path:" + sound_path)
        if sound_path == "":
            return ""
        mp3_file = FileUtils.change_ext(sound_path, Exts.EXT_MP3)
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        lip_file = FileUtils.change_ext(sound_path, Exts.EXT_LIP)
        fuz_file = FileUtils.change_ext(sound_path, Exts.EXT_FUZ)
        msg = ""
        # mp3
        if exists(mp3_file):
            msg = " mp3[ok] "
        # wav
        if exists(wav_file):
            msg += " wav[ok] "
        else:
            msg += "wav[missing] "
        # xwm
        if exists(xwm_file):
            msg += "xmw[ok] "
        else:
            msg += "xmw[missing] "
        # lip
        if exists(lip_file):
            msg += "lip[ok] "
        else:
            msg += "lip[missing] "
        # fuz
        if exists(fuz_file):
            msg += "fuz[ok] "
        else:
            msg += "fuz[missing] "
        return msg

    def set_sound(self, sound_path: str):
        """
        Screen Element: Select row
        :param sound_path:
        :return:
        """
        self._console_add("set_sound() sound_path: " + sound_path)
        self._log.debug("-- set_sound() sound_path:" + sound_path)
        if sound_path.strip() == "":
            return
        ret_val = self.encoder.try_to_gen_wav(sound_path, force_generation=False)
        if ret_val == SkyAudioEncoder.RET_SUCCESS:
            wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
            self.player.set(wav_file)
        else:
            ret_msg = self.encoder.get_last_error()
            err_description = self.encoder.get_last_stdout()
            popup_text = "Error selecting track " + sound_path + ": " + ret_msg + "\n\n" + err_description
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title="Play Audio Error")
            self._console_add(popup_text)

    def play_sound(self, sound_path: str):
        """
        Screen Element: Play Button
        :param sound_path:
        :return:
        """
        self._console_add("play_sound() sound_path: " + sound_path)
        self._log.debug("-- play_sound() sound_path:" + sound_path)
        if sound_path == "":
            popup_text = "No sound file selected."
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)
            self._console_add(popup_text)
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
            self._console_add(popup_text)

    def stop_sound(self):
        """
        Screen Element: Stop Button
        :return:
        """
        self._console_add("stop_sound()")
        self._log.debug("-- stop_sound()")
        self.player.stop()

    def pause_sound(self):
        """
        Screen Element: Pause Button
        :return:
        """
        self._console_add("pause_sound()")
        self._log.debug("-- stop_sound()")
        self.player.pause()

    def set_volume(self, volume: int):
        """
        Screen Element: Volume bar.
        :param volume:
        :return:
        """
        self._console_add("set_volume() volume:" + str(volume))
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
        self._console_add("open_folder() sound_path:" + sound_path)
        mp3_file = FileUtils.change_ext(sound_path, Exts.EXT_MP3)
        lip_file = FileUtils.change_ext(sound_path, Exts.EXT_LIP)
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
        if exists(lip_file):
            FileUtils.open_file_on_file_explorer(lip_file)
            return
        if exists(mp3_file):
            FileUtils.open_file_on_file_explorer(mp3_file)
            return
        popup_text = "File " + sound_path + " not found."
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
        self._console_add(popup_text)

    def copy_track_name(self, sound_path: str):
        """
        Copy the track name to the clipboard.
        :param sound_path:
        :return:
        """
        self._console_add("copy_track_name() sound_path:" + sound_path)
        self._log.debug("-- copy_track_name()")
        pyperclip.copy(sound_path)
        popup_text = "Track name " + sound_path + " was copied to the clipboard."
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)
        self._console_add(popup_text)

    def copy_track_info(self, sound_path: str, list_audio_data):
        """
        Copy track info to clipboard.
        :param sound_path:
        :param list_audio_data:
        """
        self._log.debug("-- copy_track_info()")
        self._console_add("copy_track_info() sound_path:" + sound_path)
        data: AudioData
        out_data = ""
        for data in list_audio_data:
            if data.file_path == sound_path:
                out_data = data.to_string()
        pyperclip.copy(out_data)
        popup_text = "Track information as copied to the clipboard: \n" + out_data
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)
        self._console_add(popup_text)

    def audio_gen_lip(self, sound_path: str, list_audio_data):
        "NOT WORKING PROPERLY"
        self._log.debug("-- audio_gen_lip()")
        self._console_add("audio_gen_lip() sound_path:" + sound_path)
        data: AudioData
        subtitles = ""
        wavfile = sound_path + ".wav"
        if exists(wavfile) != True:
            msg = "Error, could not find WAV file " + wavfile + " required to generate the lip file!"
            self._log.warning("**WARNING** " + msg)
            self._console_add(msg)
            sg.popup_ok_cancel(msg, keep_on_top=True, icon=self.app.app_icon_ico,
                               title=AudioLogicLayer.STR_ERROR_POPUP)
            return False
        for data in list_audio_data:
            if data.file_path == sound_path:
                subtitles = data.subtitle
        # 0 - Creation Kit Exe
        # 1 - WAV file
        # 3 - Subtitle
        cmd = "{0}  -GenerateSingleLip:\"{1}\" \"{2}\"".format(self.app.creation_kit_exe, sound_path, subtitles)
        # print("##############" + cmd)

    def audio_gen_xwm(self, sound_path: str):
        """
        Generate XWM file.
        :param sound_path:
        """
        self._log.debug("-- audio_gen_xwm()")
        self._console_add("audio_gen_xwm(): " + sound_path)
        if sound_path.strip() == "":
            popup_text = "Error: No sound file selected!"
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                     title=AudioLogicLayer.STR_INFO_POPUP)
            self._console_add(popup_text)
            return
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        # in case a XWM file already exists, ask first
        if exists(xwm_file):
            popup_text = "The following file is going to be overwritten: \n" + str(xwm_file) +\
                         "\n\nDo you want to continue?"
            popup_ret = sg.popup_ok_cancel(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                                 title=AudioLogicLayer.STR_INFO_POPUP)
            self._console_add(popup_text)
            if popup_ret == AudioLogicLayer.STR_CANCEL:
                return
        # XWM file is going to be generated!
        # in case WAV does not exist, create one
        ret_flag = True
        ret_int = SkyAudioEncoder.RET_SUCCESS
        ret_msg = ""
        ret_stdout = ""
        if not exists(wav_file):
            [ret_flag, ret_val, ret_msg, ret_stdout] = self._generate_wav_if_not_exit(sound_path, xwm_to_wav=False)
        if not ret_flag:
            self._log.warn("Last Stdout:" + ret_stdout)
            self._log.warn("Last error:" + ret_msg + " for sound_path:" + sound_path)
            self._console_add("Last Stdout:\n" + ret_stdout)
            self._console_add("Last error:\n" + ret_msg + " for sound_path:" + sound_path)
            popup_text = "Error Generating XWM file: Error creating WAV file.\nSound Path: " + sound_path + \
                         "\nError Message:" + ret_msg
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            self._console_add(popup_text)
            return
        ret_val = self.encoder.wav_to_xwm(sound_path)
        ret_stdout = self.encoder.get_last_stdout()
        ret_msg = self.encoder.get_last_error()
        self._log.warn("Last Stdout:\n" + ret_stdout)
        self._console_add("Last Stdout:\n" + ret_stdout)
        if ret_val != SkyAudioEncoder.RET_SUCCESS:
            self._log.error("Last error:" + ret_msg + " for sound_path:" + sound_path)
            self._console_add("Last error:" + ret_msg + " for sound_path:" + sound_path)
            popup_text = "Error encoding WAV into XWM.\nSound Path:" + sound_path + "\nError Code:" + str(ret_val) + \
                         ".\nError Message:" + ret_msg
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                     title=AudioLogicLayer.STR_ERROR_POPUP)
            self._console_add(popup_text)
            return
        popup_text = "Success generating XWM file."
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)
        self._console_add(popup_text)

    def audio_gen_fuz(self, sound_path: str):
        """
        Generate fuz file.
        :param sound_path:
        :return:
        """
        self._log.debug("-- audio_gen_fuz()")
        self._console_add("audio_gen_fuz() sound_path:" + sound_path)
        fuz_file = FileUtils.change_ext(sound_path, Exts.EXT_FUZ)
        ret_val = self.encoder.fuz(sound_path)
        if ret_val != SkyAudioEncoder.RET_SUCCESS:
            popup_text = "Error encoding file into FUZ format: " + self.encoder.get_last_error()
            self._log.error("PopUp Error: " + popup_text)
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            self._console_add(popup_text)
            return
        self._log.debug("FUZ file " + fuz_file + " generated successfully!")
        popup_text = "Success generating FUZ file " + fuz_file + "."
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)
        self._console_add(popup_text)

    def audio_gen_fuz_all(self, list_sound_path, parallel_method: int, ask_popup=True):
        """
        Execute fuz command massively, and returns a report.
        Tests with parallel methods, using the same dataset:
        *Method 1*
        (1) QuickTimer: 32.77095009999999 seconds
        (2) QuickTimer: 19.1045664 seconds (after restart, fow apps)
        (3) QuickTimer: 21.5257244 seconds (no restart, few apps)
        *Method 2*
        (1) QuickTimer: 29.6214035 seconds (many apps opened)
        (2) QuickTimer: 25.2366236 seconds (after restart, fow apps)
        (3) QuickTimer: 15.642155099999997 seconds (no restart, few apps)
        :param list_sound_path:
        :param parallel_method: 1 for one thread per core, 2 for thread ThreadPool (built-in).
        :return:
        """
        self._log.debug("audio_gen_fuz_all()")
        self._console_add("audio_gen_fuz_all()")
        # popup of confirmation
        if ask_popup:
            popup_text = "This procedure will overwrite any .fuz and xwm pre-existing file.\n If the audios are recoded in mp3 format, wav files are going to be overwritten as well.\n\n Do you want to continue?"
            self._console_add(popup_text)
            self._log.debug("popup_text:" + popup_text)
            popup_ret = sg.popup_ok_cancel(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                                           title=AudioLogicLayer.STR_INFO_POPUP)
            self._console_add("User option: " + popup_ret)
            if popup_ret == AudioLogicLayer.STR_CANCEL:
                return
        # init the batch generation
        self._console_add("audio_gen_fuz_all() list_sound_path:" + str(list_sound_path) + ", parallel_method:" +
                          str(parallel_method))
        curr_exec_path = self.encoder.get_exe_dir()
        report_list_arg = []
        report_list_async = []
        ncores = multiprocessing.cpu_count()
        if ncores <= 1:
            ncores = 2
        self._console_add("-- ncores:" + str(ncores))
        # print("-- ncores:" + str(ncores))
        splitted_list = split_list(list_sound_path, ncores)
        # Thread managing, one per core
        if parallel_method != 2:
            threads = []
            ret_list = []
            for small_list in splitted_list:
                process = Thread(target=AudioLogicLayer._exec_fuz_list, args=[small_list, curr_exec_path, report_list_arg])
                process.start()
                threads.append(process)
            for process in threads:
                process.join()
        # Builtin thread pool
        else:
            pool = ThreadPool()
            async_result_list = []
            for small_list in splitted_list:
                async_result = pool.apply_async(AudioLogicLayer._exec_fuz_list, (small_list, curr_exec_path, report_list_arg))
                async_result_list.append(async_result)
            for item in async_result_list:
                return_val = item.get()
                report_list_async.append(return_val)
        n_errors = ReportBatchCmd.count_errors(report_list_arg)
        n_success = ReportBatchCmd.count_success(report_list_arg)
        self._log.debug("Batch finished. n_errors:" + str(n_errors) + ", n_success:" + str(n_success))
        if ask_popup:
            popup_ret = ""
            popup_text = "Batch execution finished with {0} errors and {1} successes. Do you want to open the report?".format(n_errors, n_success)
            popup_ret = sg.popup_ok_cancel(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            self._console_add(popup_text)
            html_report = ReportBatchCmd.export_report(report_list_arg, self.app.app_dir)
            url_report = "file:///" + os.path.realpath(html_report)
            # print("url_report:" + url_report)
            # print("popup_ret:" + popup_ret)
            if popup_ret != AudioLogicLayer.STR_CANCEL:
                webbrowser.open(url_report, new=2)

    def audio_gen_silent(self, sound_path: str, list_audio_data, ask_popup=True):
        self._log.debug("-- audio_gen_silent()")
        self._console_add("audio_gen_silent(): " + sound_path)
        # (1) check if no file was selected
        if sound_path.strip() == "":
            popup_text = "Error: No sound file selected!"
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                     title=AudioLogicLayer.STR_INFO_POPUP)
            self._console_add(popup_text)
            return
        # (2) filter the right file text from table data
        audio_text = ""
        for data in list_audio_data:
            if data.file_path == sound_path:
                audio_text = data.subtitle
                break
        # (3) calc usefull info
        sound_no_ext = FileUtils.remove_ext(sound_path)
        reading_time = AudioLogicLayer._calc_reading_time(text_str=audio_text,
                                                          wpm=self.app.settings_obj.audio_wpm,
                                                          word_len=self.app.settings_obj.audio_word_len,
                                                          min_time=self.app.settings_obj.audio_min_time,
                                                          padding=self.app.settings_obj.audio_padding)
        sound_wav = sound_no_ext + ".wav"
        bkp_name = sound_no_ext + ".rand" + str(randint(10000, 99999)) + ".wav.bkp"
        file_already_exist = os.path.exists(sound_wav)
        # (4) Popup and backup
        if ask_popup and file_already_exist:
            popup_text = "Audio file " + sound_wav + " already exists. Continuing will overwrite this file.\n\n" +\
                         "New generated file are going to have " + str(reading_time) + " seconds.\n\n" +\
                         "Are you sure?\n\n"
            popup_ret = sg.popup_ok_cancel(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                                           title=AudioLogicLayer.STR_INFO_POPUP)
            if (popup_ret == AudioLogicLayer.STR_CANCEL) or (popup_ret is None):
                self._log.debug("-- audio_gen_silent() CANCELED")
                self._console_add("-- audio_gen_silent() CANCELED")
                return
            self._log.info("creating backup file " + str(bkp_name))
            self.player.reset()
            os.rename(sound_wav, bkp_name)
        # (5) GENERATE EMPTY AUDIO
        ret_val, trace = AudioLogicLayer._create_silent_audio(sound_no_ext, reading_time)
        # in case of failure, report the error and restore the backup
        if not ret_val:
            self._log.error(trace)
            sg.popup_ok(trace, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)
            if file_already_exist:
                os.rename(bkp_name, sound_wav)
            self.player.set(sound_wav)
            return
        # in case of success, delete the backup
        else:
            self._log.info("Deleting BACKUP file " + bkp_name)
            os.remove(bkp_name)
            self.player.set(sound_wav)



    def audio_unfuz(self, sound_path: str):
        """
        Decode FUZ file into lip, xwm an wav format.
        :param sound_path: sound file.
        """
        self._log.debug("-- audio_unfuz()")
        self._console_add("audio_unfuz() sound_path:" + sound_path)
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
            self._log.error("PopUp Error: " + popup_text)
            popup_ret = sg.popup_ok_cancel(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                                           title=AudioLogicLayer.STR_INFO_POPUP)
            if popup_ret == AudioLogicLayer.STR_CANCEL:
                self._log.info("Operation {0} was CANCELLED".format("audio_unfuz()"))
                self._console_add("Operation {0} was CANCELLED".format("audio_unfuz()"))
                return
        ret_val = self.encoder.unfuz(sound_path)
        if ret_val != SkyAudioEncoder.RET_SUCCESS:
            popup_text = "Error decoding file " + sound_path + "\nError Code:" + str(ret_val) + "\n. Error message:" + \
                         self.encoder.get_last_error()
            self._log.error("PopUp Error: " + popup_text)
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            self._console_add(popup_text)
            return
        self._log.debug("UNFUZ on file " + sound_path + " was successful!")
        popup_text = "Success on UNFUZ file " + sound_path + "."
        self._console_add(popup_text)
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)

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

    def console_has_change(self):
        """
        Tells if the console has any change or not.
        :return: True or false.
        """
        return self._console_has_change

    def get_console_output(self):
        """
        Retuns the string with the log execution of the last task.
        :return: string with the console output.
        """
        self._console_has_change = False
        return self.console_output

    @staticmethod
    def _exec_fuz_list(list_files, exec_path, list_exec_report):
        """
        Execute the fuz operation for all listed files on list_files. The encoder is instantiated using the exec_path
        as reference. A list of report objects BatchCmdReport is returned and is appended (extend) to the mutable list
        list_exec_report.
        :param list_files: list of sound files where are going to be applied the fuz operation.
        :param exec_path: Exec path to instantidate the SkyAudioEncoder object.
        :param list_exec_report: mutable list of execution reports.
        :return: list of execution reports generated in this thread.
        """
        encoder = SkyAudioEncoder(exec_path)
        thread_report = []
        if len(list_files) == 0:
            return thread_report
        for sound_path in list_files:
            report = ReportBatchCmd()
            fuz_file = FileUtils.change_ext(sound_path, Exts.EXT_FUZ)
            ret_val = encoder.fuz(sound_path)
            report.error_code = ret_val
            if ret_val != SkyAudioEncoder.RET_SUCCESS:
                report.error_flag = False
                report.error_message = encoder.get_last_error()
            else:
                report.error_flag = True
            report.command = encoder.get_last_command()
            report.stdout = encoder.get_last_stdout()
            report.process_code = encoder.get_last_encodder_ret_code()
            report.file_name = sound_path
            report.exe_dir = exec_path
            thread_report.append(report)
        AudioLogicLayer.batchReportMutex.acquire()
        try:
            list_exec_report.extend(thread_report)
        finally:
            AudioLogicLayer.batchReportMutex.release()
        return thread_report

    @staticmethod
    def _calc_reading_time(text_str, wpm=110, word_len=5, min_time=2, padding=0):
        """
        Estimate the reading time in seconds.
        :param text_str: Text to be read.
        :param wpm: words per minute.
        :param word_len: length of each word.
        :param min_time: minimum time.
        :param padding: this value will be added to the generated time.
        :return: extimated reading time.
        """
        # split text in words
        text_list = text_str.split()
        # count words
        total_words = 0
        for current_text in text_list:
            total_words += len(current_text) / word_len
        # calc reading time in seconds
        read_time = (total_words * 60) / wpm
        # add padding
        read_time = read_time + padding
        # ensure min time
        read_time = max([read_time, min_time])
        return round(read_time)

    @staticmethod
    def _create_silent_audio(file_name: str, duration_sec: int):
        try:
            silent_audio = AudioSegment.silent(duration=int(duration_sec) * 1000)  # or be explicit
            silent_audio.export(file_name + ".wav", format="wav")
            return True, "SUCCESS"
        except:
            ex_msg = "Error exporting file " + file_name + ".wav\n'" +\
                     "traceback.format_exc(): " + str(traceback.format_exc()) + "\n" +\
                     "sys.exc_info()[2]: " + str(sys.exc_info()[2])
            return False, ex_msg

    def _generate_wav_if_not_exit(self, sound_path, xwm_to_wav=True):
        """
        Try to generate WAV file if it does not exit.
        :param sound_path: Path of the file to be used on the generation of the wav file.
        :param xwm_to_wav: optional flag to tell the method to try or not to generate a wav file from a xwm.
        :return: return a vector [ret_flag: bool, ret_val: int, ret_msg: str, ret_stdout: str], where ret_flag is True
        if the WAV file already exits, or it was rightly generated. Returns False in case some error occurred
        generating the WAV file. ret_val is the code returned by the encoder. ret_str is the error message returned by
        the encoder, in case of error, and the ret_strout is the console output generated (error os success).
        """
        self._log.debug("-- _generate_wav_if_not_exit()")
        self._console_add("_generate_wav_if_not_exit()")
        ret_flag = False
        ret_val = SkyAudioEncoder.RET_SUCCESS
        ret_msg = ""
        ret_stdout = ""
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        mp3_file = FileUtils.change_ext(sound_path, Exts.EXT_MP3)
        self._log.debug("wav_file:" + wav_file + ", xwm_file:" + xwm_file + ", mp3_file:" + mp3_file)
        self._console_add("wav_file:" + wav_file + ", xwm_file:" + xwm_file + ", mp3_file:" + mp3_file)
        if not exists(wav_file):
            self._log.info("WAV file for <" + sound_path + "> was not found. Search for alternatives: XWM and MP3...")
            self._console_add("WAV file for <" + sound_path + "> was not found. Search for alternatives: XWM and MP3...")
            # try to generate file from XWM
            if exists(xwm_file) and xwm_to_wav:
                self._log.info("XWM was found for " + sound_path)
                self._console_add("XWM was found for " + sound_path)
                ret_val = self.encoder.xwm_to_wav(sound_path)
                ret_stdout = self.encoder.get_last_stdout()
                self._log.error("Last stdout: " + ret_stdout)
                self._console_add("Last stdout: " + ret_stdout)
                if ret_val != SkyAudioEncoder.RET_SUCCESS:
                    ret_msg = self.encoder.get_last_error()
                    self._log.error("Last error: " + ret_msg)
                    self._console_add("Last error: " + ret_msg)
            # try mp3 format
            elif exists(mp3_file):
                self._log.info("MP3 was found for " + sound_path)
                self._console_add()
                ret_val = self.encoder.mp3_to_wav(sound_path)
                ret_stdout = self.encoder.get_last_stdout()
                self._log.error("Last stdout: " + ret_stdout)
                self._console_add("Last stdout: " + ret_stdout)
                if ret_val != SkyAudioEncoder.RET_SUCCESS:
                    ret_msg = self.encoder.get_last_error()
                    self._log.error("Last error: " + ret_msg)
                    self._console_add("Last error: " + ret_msg)
            else:
                ret_msg = "WAV file does not exit for track \"" + sound_path + \
                          "\", and no alternative (xwm or mp3) was found.\n Try to use UnFuz first."
                self._log.error("ret_msg:" + ret_msg)
                self._console_add("ret_msg:" + ret_msg)
        else:
            ret_flag = True
        if ret_val == SkyAudioEncoder.RET_SUCCESS:
            ret_flag = True
        # print([ret_flag, ret_val, ret_msg, ret_stdout])
        self._console_add(str([ret_flag, ret_val, ret_msg, ret_stdout]))
        return [ret_flag, ret_val, ret_msg, ret_stdout]

    def _console_clear(self):
        self.console_output = ""
        self._console_has_change = True

    def _console_add(self, msg: str):
        self.console_output += msg + "\n"
        self._console_has_change = True





