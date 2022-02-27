import logging
import webbrowser
import PySimpleGUI as sg
from QuestExports.QuestDialogs import QuestDialogs
from PyUtils.Logger import Logger
from AppInfo import AppInfo
from AppInfo import AppSettings


class CkLogicLayer:
    """
    """
    DEFAULT_THEME = "DarkGrey13"

    def __init__(self):
        self.app = AppInfo()
        Logger.initialize(self.app.log_file, level_log=logging.DEBUG, level_console=logging.WARNING)
        _log = Logger.get()
        _log.debug("-- Initializing CkLogicLayer()")

    def export_objects_to_csv(self):
        _log = Logger.get()
        _log.debug("-- export_objects_to_csv()")
        skyrim_path = self.app.settings_obj.skyrim_path
        comments_csv = self.app.settings_obj.comments_file
        actors_csv = self.app.settings_obj.actors_file
        _log.debug(" -- QuestDialogs.export_objects_to_csvdics() skyrim_path:" + skyrim_path +\
                   ", comments_csv:" + comments_csv + ", actors_csv:" + actors_csv)
        [exported_files, list_objects, list_actors] = QuestDialogs.export_objects_to_csvdics(skyrim_path, comments_csv, actors_csv)
        poup_text = " * Files processed: "
        i = 0
        for f in exported_files:
            if i == 0:
                poup_text += "\n" + f
            else:
                poup_text += ", " + f
            i = i + 1
        i = 0
        poup_text += "\n\n * Objects founded:"
        for f in list_objects:
            if i == 0:
                poup_text += "\n" + f
            else:
                poup_text += ", " + f
            i = i + 1
        i = 0
        poup_text += "\n\n * Actors founded: "
        for f in list_actors:
            if i == 0:
                poup_text += "\n" + f
            else:
                poup_text += ", " + f
            i = i + 1
        sg.Popup(poup_text, keep_on_top=True, icon=self.app.app_icon_ico, title="Exported Objects Summary")

    def generate_documentation(self):
        _log = Logger.get()
        _log.debug("-- generate_documentation()")
        skyrim_path = self.app.settings_obj.skyrim_path
        comments_csv = self.app.settings_obj.comments_file
        actors_csv = self.app.settings_obj.actors_file
        docs_dir = self.app.settings_obj.docgen_dir
        _log.debug(" --  QuestDialogs.generate_quest_documentation() ) skyrim_path:" + skyrim_path +\
                   ", comments_csv:" + comments_csv + ", actors_csv:" + actors_csv + ", docs_dir:" + docs_dir)
        qlist = QuestDialogs.generate_quest_documentation(skyrim_path, comments_csv, actors_csv, docs_dir)
        i = 0
        poup_text = "\n * Documentation generated for the following quests:\n"
        for f in qlist:
            if i == 0:
                poup_text += "\n" + f
            else:
                poup_text += ", " + f
            i = i + 1
        sg.Popup(poup_text, keep_on_top=True, icon=self.app.app_icon_ico, title="Documentation Generation Summary")

    def open_tutorial(self):
        _log = Logger.get()
        _log.debug("-- open_tutorial()")
        url_tutorial = self.app.tutorial_url()
        _log.debug("webbrowser.open() url_tutorial:" + url_tutorial)
        webbrowser.open(url_tutorial, new=2)

    def open_github(self):
        _log = Logger.get()
        _log.debug("-- open_github()")
        url = self.app.url_github
        _log.debug("webbrowser.open() url_tutorial:" + url)
        webbrowser.open(url, new=2)

    def open_nexus(self):
        _log = Logger.get()
        _log.debug("-- open_nexus()")
        url = self.app.url_nexus
        _log.debug("webbrowser.open() url_tutorial:" + url)
        webbrowser.open(url, new=2)

    def open_theme_picker(self):
        _log = Logger.get()
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
                sg.Popup('Please, close the Application to apply the Theme: ' + selected_theme, keep_on_top=True, icon=self.app.app_icon_ico, title="Attention!")
                return selected_theme
            elif event == "RESET":
                selected_theme = CkLogicLayer.DEFAULT_THEME
                _log.debug("THEME SELECTED:" + selected_theme)
                self.app.settings_obj.app_theme = selected_theme
                self.app.settings_obj.save()
                window_picker.close()
                sg.Popup('Please, close the Application to apply the Theme: ' + selected_theme, keep_on_top=True, icon=self.app.app_icon_ico, title="Attention!")
                return selected_theme
            sg.theme(values['-LIST-'][0])
            sg.popup_get_text('This is {}'.format(values['-LIST-'][0]))
            selected_theme = values['-LIST-'][0]
            _log.debug("*** " + values['-LIST-'][0])

    def open_settings_window(self):
        _log = Logger.get()
        _log.debug("-- open_settings_window()")
        layout = []
        # 0
        layout.append([sg.Text("Skyrim Path"), sg.InputText(default_text=self.app.settings_obj.skyrim_path)])
        # 1
        layout.append([sg.Text("Docgen Folder"), sg.InputText(default_text=self.app.settings_obj.docgen_dir)])
        # 2
        layout.append([sg.Text("Actors File"), sg.InputText(default_text=self.app.settings_obj.actors_file)])
        # 3
        layout.append([sg.Text("Comments File"), sg.InputText(default_text=self.app.settings_obj.comments_file)])
        # 4
        layout.append([sg.Text("Sort By Name(true) or FormId(false)"), sg.InputText(default_text=self.app.settings_obj.topic_sort_by_name)])
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
                self.app.settings_obj.topic_sort_by_name = values[4]
                self.app.settings_obj.save()
                window_settings.close()
                return "saved"
            elif event == "Reset":
                self.app.settings_obj.reset_and_save()
                window_settings.close()
                return "reset"

if __name__ == '__main__':
    print("oi")