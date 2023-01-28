import json
import os
import logging
from PyUtils.Obj2Json import Obj2Json
from Settings.AppSettings import AppSettings
from PyUtils.Logger import Logger


def global_app_configuration():
    """
    Initializes the logger singleton.
    :return:
    """
    AppInfo.configure(".\\App\\")
    app_info = AppInfo()
    Logger.initialize(app_info.log_file, level_log=logging.DEBUG, level_console=logging.INFO)


class AppInfo:
    """Store non-configurable settings and global constants of the application."""
    # constants
    APP_NAME_SHORT = "CKsQuestDialogManager"
    APP_NAME_LARGE = "CreationKit's Quest Dialog Manager"
    APP_VERSION = "v0.3.0.0"
    APP_VERSION_NAME = "Apple Dumpling"
    # static
    default_app_dir = ".\\App\\"

    def __init__(self, app_dir=""):
        if app_dir == "":
            app_dir = AppInfo.default_app_dir
        self.app_dir = os.path.abspath(app_dir) + "\\"
        self.audio_encoder_dir = self.app_dir + "Bin\\"
        self.img_dir = self.app_dir + "Docs\\Img\\"
        self.pages_dir = self.app_dir + "Docs\\"
        self.log_dir = self.app_dir + "Logs\\"
        self.db_dir = self.app_dir + "Db\\"
        self.csv_actors = self.db_dir + "Actors.csv"
        self.csv_comments = self.db_dir + "Comments.csv"
        self.csv_scene_order = self.db_dir + "SceneOrder.csv"
        self.app_icon_ico = self.img_dir + "Snowberry_crostata_Blur_WinIcon.ico"
        self.app_icon_png = self.img_dir + "Snowberry_crostata.png"
        self.log_file = self.log_dir + "ck-dialog-docgen.log"
        self.url_github = "https://github.com/AndersonPaschoalon/CKsQuestDialogManager.git"
        self.url_nexus = "https://www.nexusmods.com/skyrim"
        self.tutorial_html = self.pages_dir + "index.html"
        self.settings_file = self.app_dir + "settings.xml"
        self.profiles_file = self.app_dir + "profiles.xml"
        self.label_main_window = "Quest Dialog Manager for CK"
        self.label_audio_window = "Quest Audio Manager for CK"
        self.app_version = AppInfo.APP_VERSION + " -- " + AppInfo.APP_VERSION_NAME
        self.app_name_short = AppInfo.APP_NAME_SHORT
        self.app_name_LARGE = AppInfo.APP_NAME_LARGE
        self.license = self.app_dir + "Docs\\LICENSE.md"
        self.settings_obj = AppSettings(self.settings_file)
        self.creation_kit_exe = self.settings_obj.skyrim_path + "\\CreationKit.exe"

    def tutorial_url(self):
        url_tutorial = "file:///" + os.path.realpath(self.tutorial_html)
        return url_tutorial

    def to_string(self):
        obj = Obj2Json()
        obj.add("app_dir", self.app_dir)
        obj.add("img_dir", self.img_dir)
        obj.add("pages_dir", self.pages_dir)
        obj.add("log_dir", self.log_dir)
        obj.add("csv_actors", self.csv_actors)
        obj.add("csv_comments", self.csv_comments)
        obj.add("csv_scene_order", self.csv_scene_order)
        obj.add("app_icon_ico", self.app_icon_ico)
        obj.add("app_icon_png", self.app_icon_png)
        obj.add("log_file", self.log_file)
        obj.add("tutorial_html", self.tutorial_html)
        obj.add("settings_file", self.settings_file)
        obj.add("profiles_file", self.profiles_file)
        obj.add("label_main_window", self.label_main_window)
        obj.add("label_audio_window", self.label_audio_window)
        obj.add("app_version", self.app_version)
        # settings = str(self.settings_obj.data)
        # obj.add("settings_obj", settings)
        return obj.json()

    def reload(self):
        """
        Reload information from configuration file.
        """
        self.settings_obj = AppSettings(self.settings_file)
        self.creation_kit_exe = self.settings_obj.skyrim_path + "\\CreationKit.exe"

    @staticmethod
    def configure(app_dir):
        AppInfo.default_app_dir = app_dir


if __name__ == '__main__':
    aa = AppInfo()
    print(aa.to_string())
    aa.settings_obj.docgen_dir = "../OUTPUT/"
    aa.settings_obj.save()
