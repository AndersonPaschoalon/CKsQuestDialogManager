import datetime
import os
import PySimpleGUI as sg
import pyperclip
from os.path import exists
from PyUtils.SkyAudioEncoder import SkyAudioEncoder
from PyUtils.MusicUtils import MusicUtils
from PyUtils.FileUtils import FileUtils
from PyUtils.FileUtils import Exts
from PyUtils.Functions import *
from Gui.AudioData import AudioData
from PyUtils.Logger import Logger
from Gui.AppInfo import AppInfo
from PyUtils.Obj2Json import Obj2Json
from QuestExports.QuestDialogs import QuestDialogs
from QuestExports.Scene import Scene
from QuestExports.SceneTopic import SceneTopic
from QuestExports.BranchDialogs import BranchDialogs
from QuestExports.TopicDialogs import TopicDialogs
import multiprocessing
import threading
from threading import Thread
from threading import Lock
from multiprocessing.pool import ThreadPool
from Gui.BatchCmdReport import BatchCmdReport


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
        self.console_output = ""
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

    def play_sound(self, sound_path: str):
        """
        Screen Element: Play Button
        :param sound_path:
        :return:
        """
        self._console_add("play_sound: " + sound_path)
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
        self._console_add("stop_sound")
        self._log.debug("-- stop_sound()")
        self.player.stop()

    def pause_sound(self):
        """
        Screen Element: Pause Button
        :return:
        """
        self._console_add("pause_sound")
        self._log.debug("-- stop_sound()")
        self.player.pause()


    def set_volume(self, volume: int):
        """
        Screen Element: Volume bar.
        :param volume:
        :return:
        """
        self._console_add("set_volume " + str(volume))
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
        self._log.debug("-- audio_gen_xwm()")
        if sound_path.strip() == "":
            popup_text = "Error: No sound file selected!"
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                     title=AudioLogicLayer.STR_INFO_POPUP)
            return
        xwm_file = FileUtils.change_ext(sound_path, Exts.EXT_XWM)
        wav_file = FileUtils.change_ext(sound_path, Exts.EXT_WAV)
        # in case a XWM file already exists, ask first
        if exists(xwm_file):
            popup_text = "The following file is going to be overwritten: \n" + str(xwm_file) +\
                         "\n\nDo you want to continue?"
            popup_ret = sg.popup_ok_cancel(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                                 title=AudioLogicLayer.STR_INFO_POPUP)
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
            self._console_add("Last Stdout:" + ret_stdout)
            self._console_add("Last error:" + ret_msg + " for sound_path:" + sound_path)
            popup_text = "Error Generating XWM file: Error creating WAV file.\nSound Path: " + sound_path + \
                         "\nError Message:" + ret_msg
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            return
        ret_val = self.encoder.wav_to_xwm(sound_path)
        ret_stdout = self.encoder.get_last_stdout()
        ret_msg = self.encoder.get_last_error()
        self._log.warn("Last Stdout:" + ret_stdout)
        self._console_add("Last Stdout:" + ret_stdout)
        if ret_val != SkyAudioEncoder.RET_SUCCESS:
            self._log.error("Last error:" + ret_msg + " for sound_path:" + sound_path)
            self._console_add("Last error:" + ret_msg + " for sound_path:" + sound_path)
            popup_text = "Error encoding WAV into XWM.\nSound Path:" + sound_path + "\nError Code:" + str(ret_val) + \
                         ".\nError Message:" + ret_msg
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico,
                     title=AudioLogicLayer.STR_ERROR_POPUP)
            return
        popup_text = "Success generating XWM file."
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)


    def audio_gen_fuz(self, sound_path: str):
        """
        Generate fuz file.
        :param sound_path:
        :return:
        """
        self._log.debug("-- audio_gen_fuz()")
        fuz_file = FileUtils.change_ext(sound_path, Exts.EXT_FUZ)
        ret_val = self.encoder.fuz(sound_path)
        if ret_val != SkyAudioEncoder.RET_SUCCESS:
            popup_text = "Error encoding file into FUZ format: " + self.encoder.get_last_error()
            self._log.error("PopUp Error: " + popup_text)
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            return
        self._log.debug("FUZ file " + fuz_file + " generated successfully!")
        popup_text = "Success generating FUZ file " + fuz_file + "."
        sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_INFO_POPUP)

    def audio_gen_fuz_all(self, list_sound_path, parallel_method: int):
        """
        Execute fuz command massively, and returns a report.
        :param list_sound_path:
        :param parallel_method: 1 for one thread per core, 2 for thread ThreadPool (built-in).
        :return:
        """
        curr_exec_path = self.encoder.get_exe_dir()
        report_list_arg = []
        report_list_async = []
        ncores = multiprocessing.cpu_count()
        if ncores <= 1:
            ncores = 2
        print("-- ncores:" + str(ncores))
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
        n_errors = BatchCmdReport.count_errors(report_list_arg)
        n_success = BatchCmdReport.count_success(report_list_arg)
        popup_ret = ""
        popup_text = "Batch execution finished with {0} errors and {1} successes. Do you want to open the report?".format(n_errors, n_success)
        popup_ret == sg.popup_ok_cancel(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
        if popup_ret == AudioLogicLayer.STR_OK:
            BatchCmdReport.export_report(report_list_arg)

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
            report = BatchCmdReport()
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

    def audio_unfuz(self, sound_path: str):
        """
        Decode FUZ file into lip, xwm an wav format.
        :param sound_path: sound file.
        """
        self._log.debug("-- audio_unfuz()")
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
                return
        ret_val = self.encoder.unfuz(sound_path)
        print(">>>> ret_val:" + str(ret_val))
        if ret_val != SkyAudioEncoder.RET_SUCCESS:
            popup_text = "Error decoding file " + sound_path + "\nError Code:" + str(ret_val) + "\n. Error message:" + \
                         self.encoder.get_last_error()
            self._log.error("PopUp Error: " + popup_text)
            sg.Popup(popup_text, keep_on_top=True, icon=self.app.app_icon_ico, title=AudioLogicLayer.STR_ERROR_POPUP)
            return
        self._log.debug("UNFUZ on file " + sound_path + " was successful!")
        popup_text = "Success on UNFUZ file " + sound_path + "."
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
        print([ret_flag, ret_val, ret_msg, ret_stdout])
        self._console_add(str([ret_flag, ret_val, ret_msg, ret_stdout]))
        return [ret_flag, ret_val, ret_msg, ret_stdout]


    def _console_clear(self):
        self.console_output = ""
        self._console_has_change = True


    def _console_add(self, msg: str):
        self.console_output += msg + "\n"
        self._console_has_change = True




