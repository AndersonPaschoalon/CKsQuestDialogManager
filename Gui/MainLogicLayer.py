import os
import webbrowser
import traceback
import sys
import subprocess
import PySimpleGUI as sg
from multiprocessing import Process
from PyUtils.Logger import Logger
from PyUtils.CsvDicEditor import CsvDicEditor
from QuestExports.QuestDialogs import QuestDialogs
from QuestExports.Scene import Scene
from QuestExports.SkyrimRepository import SkyrimRepository
from Settings.AppInfo import AppInfo
from Settings.ProfileManager import ProfileManager
from Gui.CsvReorderWindow import CsvReorderWindow
from Gui.AboutWindow import AboutWindow
from Gui.AudioWindow import AudioWindow
from Gui.AppEditorCmd import AppEditorCmd
from Gui.LicenseWindow import LicenseWindow
from Gui.ProfilesWindow import ProfilesWindow


class MainLogicLayer:
    """
    """
    # DEFAULT_THEME = "DarkGrey13"
    DEFAULT_THEME = "DarkBlue12"
    POPUP_TEXT_MAX_LEN = 1200

    def __init__(self):
        self.app = AppInfo()
        self.profile_manager = ProfileManager(self.app.app_dir)
        # Logger.initialize(self.app.log_file, level_log=logging.DEBUG, level_console=logging.WARNING)
        _log = Logger.get()
        _log.debug("-- Initializing CkLogicLayer()")

    def import_from_creation_kit(self):
        skyrim_root = self.app.settings_obj.skyrim_path
        local_db = self.profile_manager.profile_db_dir()
        SkyrimRepository.import_skyrim_files(skyrim_root=skyrim_root, local_root=local_db)
        self.export_objects_to_csv(skyrim_path=local_db)

    def export_objects_to_csv(self, skyrim_path):
        _log = Logger.get()
        try:
            _log.debug("-- export_objects_to_csv()")
            # skyrim_path = self.app.settings_obj.skyrim_path
            comments_csv = self.app.settings_obj.comments_file
            actors_csv = self.app.settings_obj.actors_file
            scene_order_csv = self.app.settings_obj.scene_order_file
            _log.debug(" -- QuestDialogs.export_objects_to_csvdics() skyrim_path:" + skyrim_path + \
                       ", comments_csv:" + comments_csv + ", actors_csv:" + actors_csv)
            [exported_files, list_objects, list_actors] = QuestDialogs.export_objects_to_csvdics(skyrim_path,
                                                                                                 comments_csv,
                                                                                                 actors_csv)
            _log.debug(" -- QuestDialogs.export_scenes_data_to_csvdic()")
            [all_scene_files, quest_scenes_no_duplicates, list_scenes, list_alias] = \
                Scene.export_scenes_data_to_csvdic(skyrim_path, scene_order_csv, comments_csv,
                                                   actors_csv)
            exported_files.extend(all_scene_files)
            list_objects.extend(list_scenes)
            list_actors.extend(list_alias)
            poup_text = " * Files processed: "
            i = 0
            for f in exported_files:
                if i == 0:
                    poup_text += "\n" + f
                else:
                    poup_text += ", " + f
                i = i + 1
            i = 0
            poup_text += "\n\n * Objects found:"
            for f in list_objects:
                if i == 0:
                    poup_text += "\n" + f
                else:
                    poup_text += ", " + f
                i = i + 1
            i = 0
            poup_text += "\n\n * Actors found: "
            for f in list_actors:
                if i == 0:
                    poup_text += "\n" + f
                else:
                    poup_text += ", " + f
                i = i + 1
            _log.info("** IMPORT OBJECT FROM CREATION KIT SUMMARY: " + poup_text)
            poup_text = self._popup_text(poup_text)
            sg.Popup(poup_text, keep_on_top=True, icon=self.app.app_icon_ico, title="Exported Objects Summary")
        except:
            self._exception_handler("CkLogicLayer.export_objects_to_csv()")

    def generate_documentation(self, skyrim_path):
        _log = Logger.get()
        try:
            _log.debug("-- generate_documentation()")
            # skyrim_path = self.app.settings_obj.skyrim_path
            comments_csv = self.app.settings_obj.comments_file
            actors_csv = self.app.settings_obj.actors_file
            scene_order_csv = self.app.settings_obj.scene_order_file
            docs_dir = self.app.settings_obj.docgen_dir
            app_name = self.app.app_name_short
            github_url = self.app.url_github
            _log.debug(" --  QuestDialogs.generate_quest_documentation() ) skyrim_path:" + skyrim_path +
                       ", comments_csv:" + comments_csv + ", actors_csv:" + actors_csv + ", docs_dir:" + docs_dir +
                       ", scene_order_csv:" + scene_order_csv)
            qlist = QuestDialogs.generate_quest_documentation(skyrim_path, comments_csv, actors_csv,
                                                              scene_order_csv, docs_dir, app_name, github_url)
            i = 0
            poup_text = "\n * Documentation generated for the following quests:\n"
            for f in qlist:
                if i == 0:
                    poup_text += "\n" + f
                else:
                    poup_text += ", " + f
                i = i + 1
            _log.info("** DOCUMENT GENERATION SUMMARY: " + poup_text)
            poup_text = self._popup_text(poup_text)
            sg.Popup(poup_text, keep_on_top=True, icon=self.app.app_icon_ico, title="Documentation Generation Summary")
        except:
            self._exception_handler("CkLogicLayer.generate_documentation()")

    def open_tutorial(self):
        _log = Logger.get()
        try:
            _log.debug("-- open_tutorial()")
            url_tutorial = self.app.tutorial_url()
            _log.debug("webbrowser.open() url_tutorial:" + url_tutorial)
            webbrowser.open(url_tutorial, new=2)
        except:
            self._exception_handler("CkLogicLayer.open_tutorial()")

    def open_github(self):
        _log = Logger.get()
        try:
            _log.debug("-- open_github()")
            url = self.app.url_github
            _log.debug("webbrowser.open() url_tutorial:" + url)
            webbrowser.open(url, new=2)
        except:
            self._exception_handler("CkLogicLayer.open_github()")

    def open_nexus(self):
        try:
            _log = Logger.get()
            _log.debug("-- open_nexus()")
            url = self.app.url_nexus
            _log.debug("webbrowser.open() url_tutorial:" + url)
            webbrowser.open(url, new=2)
        except:
            self._exception_handler("CkLogicLayer.open_nexus()")

    def open_theme_picker(self):
        _log = Logger.get()
        try:
            _log.debug("-- open_theme_picker()")
            layout = [[sg.Text('Theme Browser')],
                      [sg.Text('Click a Theme color to see demo window')],
                      [sg.Listbox(values=sg.theme_list(), size=(20, 12), key='-LIST-', enable_events=True)],
                      [sg.Button('OK'), sg.Button('RESET')]]
            window_picker = sg.Window('Theme Browser', layout, icon=self.app.app_icon_ico)
            selected_theme = ""
            while True:  # Event Loop
                event, values = window_picker.read()
                if event in (sg.WIN_CLOSED, 'Exit'):
                    window_picker.close()
                    return ""
                elif event == "OK":
                    _log.debug("THEME SELECTED:" + selected_theme)
                    self.app.settings_obj.app_theme = selected_theme
                    self.app.settings_obj.save()
                    window_picker.close()
                    sg.Popup('Please, close the Application to apply the Theme: ' + selected_theme, keep_on_top=True,
                             icon=self.app.app_icon_ico, title="Attention!")
                    return selected_theme
                elif event == "RESET":
                    selected_theme = MainLogicLayer.DEFAULT_THEME
                    _log.debug("THEME SELECTED:" + selected_theme)
                    self.app.settings_obj.app_theme = selected_theme
                    self.app.settings_obj.save()
                    window_picker.close()
                    sg.Popup('Please, close the Application to apply the Theme: ' + selected_theme, keep_on_top=True,
                             icon=self.app.app_icon_ico, title="Attention!")
                    return selected_theme
                sg.theme(values['-LIST-'][0])
                sg.popup_get_text('This is {}'.format(values['-LIST-'][0]))
                selected_theme = values['-LIST-'][0]
                _log.debug("*** " + values['-LIST-'][0])
        except:
            self._exception_handler("CkLogicLayer.open_theme_picker()")

    def open_settings_window(self):
        _log = Logger.get()
        try:
            _log.debug("-- open_settings_window()")
            layout = []
            # 0
            layout.append([sg.Text("Skyrim Path"), sg.InputText(default_text=self.app.settings_obj.skyrim_path)])
            # 1
            layout.append([sg.Text("Docgen Folder"), sg.InputText(default_text=self.app.settings_obj.docgen_dir)])
            # 2
            layout.append([sg.Text("Actors.csv File"), sg.InputText(default_text=self.app.settings_obj.actors_file)])
            # 3
            layout.append([sg.Text("Comments.csv File"), sg.InputText(default_text=self.app.settings_obj.comments_file)])
            # 4
            layout.append([sg.Text("SceneOrder.csv File"), sg.InputText(default_text=self.app.settings_obj.scene_order_file)])
            # 5
            layout.append([sg.Text("Sort By Name(true) or FormId(false)"),
                           sg.InputText(default_text=self.app.settings_obj.topic_sort_by_name)])
            layout.append([sg.Button('Save'), sg.Button('Reset'), sg.Button('Cancel')])
            window_settings = sg.Window('Settings Window', layout, icon=self.app.app_icon_ico)
            while True:  # Event Loop
                event, values = window_settings.read()
                if event in (sg.WIN_CLOSED, 'Exit', 'Cancel'):
                    window_settings.close()
                    return ""
                elif event == "Save":
                    self.app.settings_obj.skyrim_path = values[0]
                    self.app.settings_obj.docgen_dir = values[1]
                    self.app.settings_obj.actors_file = values[2]
                    self.app.settings_obj.comments_file = values[3]
                    self.app.settings_obj.scene_order_file = values[4]
                    self.app.settings_obj.topic_sort_by_name = values[5]
                    self.app.settings_obj.save()
                    window_settings.close()
                    return "saved"
                elif event == "Reset":
                    self.app.settings_obj.reset_and_save()
                    window_settings.close()
                    return "reset"
        except:
            self._exception_handler("CkLogicLayer.open_settings_window()")
            return "exception"

    def open_profile_window(self):
        profiles = ProfilesWindow(self.app.app_dir)
        return profiles.run()

    def get_profile_name(self):
        profiles = ProfilesWindow(self.app.app_dir)
        return profiles.get_active_profile_name()

    def open_about_window(self):
        about = AboutWindow(self.app.app_dir)
        about.run()

    def open_license_window(self):
        about = LicenseWindow(self.app.app_dir)
        about.run()

    def open_actors_editor(self):
        _log = Logger.get()
        _log.debug("-- open_actors_editor() start")
        cmd = AppEditorCmd(self.app.settings_obj.csv_editor_cmd)
        if cmd.is_process():
            _log.debug("-- _exec_actor_editor() process start")
            p = Process(target=self._exec_actor_editor)
            p.start()
            p.join()
            _log.debug("-- _exec_actor_editor() process finish")
        else:
            cmd_str = cmd.get_batch(self.app.settings_obj.actors_file)
            _log.debug("command: " + cmd_str)
            # print(cmd_str)
            subprocess.Popen(cmd_str)
        _log.debug("-- open_actors_editor() finish")

    def open_comments_editor(self):
        _log = Logger.get()
        _log.debug("-- open_actors_editor() start")
        cmd = AppEditorCmd(self.app.settings_obj.csv_editor_cmd)
        if cmd.is_process():
            _log.debug("-- _exec_comments_editor() process start")
            p = Process(target=self._exec_comments_editor)
            p.start()
            p.join()
            _log.debug("-- _exec_comments_editor() process finish")
        else:
            cmd_str = cmd.get_batch(self.app.settings_obj.comments_file)
            _log.debug("command: " + cmd_str)
            # print(cmd_str)
            subprocess.Popen(cmd_str)
        _log.debug("-- open_actors_editor() finish")

    def open_scenes_editor(self):
        reorder = CsvReorderWindow(self.app.app_dir)
        reorder.run(self.app.settings_obj.scene_order_file)

    def launch_audio_manager(self):
        _log = Logger.get()
        try:
            _log.debug("-- launch_audio_manager()")
            audio_window = AudioWindow(self.app.app_dir)
            audio_window.run()
        except:
            self._exception_handler("CkLogicLayer.launch_audio_manager()")

    def _exec_actor_editor(self):
        _log = Logger.get()
        _log.debug("-- _exec_actor_editor() start")
        editor = CsvDicEditor()
        editor.run_app(self.app.settings_obj.actors_file)
        _log.debug("-- _exec_actor_editor() finish")

    def _exec_comments_editor(self):
        _log = Logger.get()
        _log.debug("-- open_comments_editor() start")
        editor = CsvDicEditor()
        editor.run_app(self.app.settings_obj.comments_file)
        _log.debug("-- _exec_comments_editor() finish")

    def _popup_text(self, popup_raw_text):
        """
        Just format the text into a smaller and displayable size
        :param popup_raw_text: text to be displayed.
        :return:
        """
        if len(popup_raw_text) > MainLogicLayer.POPUP_TEXT_MAX_LEN:
            poup_text_display = popup_raw_text[:MainLogicLayer.POPUP_TEXT_MAX_LEN] + "..."
        else:
            poup_text_display = popup_raw_text
        return poup_text_display

    def _exception_handler(self, error_method):
        _log = Logger.get()
        err_title = "** Error on method " + error_method + " **"
        err_msg = "** Error details: **\n"
        err_msg += "traceback.format_exc():\n" + str(traceback.format_exc()) + "\n"
        err_msg += "sys.exc_info():\n" + str(sys.exc_info()[2]) + "\n"
        sg.Popup(err_msg,
                 keep_on_top=True,
                 icon=self.app.app_icon_ico,
                 title=err_title)
        _log.error(err_title)
        _log.error(traceback.format_exc())
        _log.error(sys.exc_info()[2])


# if __name__ == '__main__':
#     print("oi")
