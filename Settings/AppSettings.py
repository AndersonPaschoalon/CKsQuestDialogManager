import json
import os
import logging
import lxml.etree as ET
from PyUtils.Obj2Json import Obj2Json


class AppSettings:
    """
    Store all configurable settings from the application.
    """
    SKYRIM_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Skyrim"
    DOGEN_DIR = ".\\OUTPUT\\"
    LOG_LEVEL = "DEBUG"
    ACTORS_FILE = "App\\Db\\Actors.csv"
    COMMENTS_FILE = "App\\Db\\Comments.csv"
    SCENE_ORDER_FILE = "App\\Db\\SceneOrder.csv"
    TOPIC_SORT_BY_NAME = "true"
    DEFAULT_THEME = "DarkBlue12"
    CSV_EDITOR_CMD = "Default"
    AUDIO_WPM = 110
    AUDIO_WORD_LEN = 5
    AUDIO_MIN_TIME = 2
    AUDIO_PADDING = 1

    def __init__(self, settings_file):
        self.settings_file = settings_file
        tree = ET.parse(self.settings_file)
        root = tree.getroot()
        self.reset()
        for child in root:
            if child.tag == "skyrim-path":
                self.skyrim_path = child.text
            elif child.tag == "dogen-dir":
                self.docgen_dir = os.path.abspath(child.text)
            elif child.tag == "log-level":
                self.log_level = child.text
            elif child.tag == "actors-file":
                self.actors_file = child.text
            elif child.tag == "comments-file":
                self.comments_file = child.text
            elif child.tag == "scene-order-file":
                self.scene_order_file = child.text
            elif child.tag == "topic-sort-by-name":
                self.topic_sort_by_name = child.text
            elif child.tag == "app-theme":
                self.app_theme = child.text
            elif child.tag == "csv-editor-cmd":
                self.csv_editor_cmd = child.text
            elif child.tag == "audio-wpm":
                self.audio_wpm = int(child.text)
            elif child.tag == "audio-word-len":
                self.audio_word_len = int(child.text)
            elif child.tag == "audio-min-time":
                self.audio_min_time = int(child.text)
            elif child.tag == "audio-padding":
                self.audio_padding = int(child.text)
        # derivated settings
        self.docgen_dir_md = os.path.join(self.docgen_dir, "Md")
        self.docgen_dir_json = os.path.join(self.docgen_dir, "Json")
        self.docgen_dir_html = os.path.join(self.docgen_dir, "Html")
        self.docgen_dir_docx = os.path.join(self.docgen_dir, "Docx")
        self.docgen_reports = os.path.join(self.docgen_dir, "Reports")

    def save(self):
        tree = ET.parse(self.settings_file)
        root = tree.getroot()
        for child in root:
            if child.tag == "skyrim-path":
                child.text = self.skyrim_path
            elif child.tag == "dogen-dir":
                child.text = str(self.docgen_dir)
            elif child.tag == "log-level":
                child.text = self.log_level
            elif child.tag == "actors-file":
                child.text = self.actors_file
            elif child.tag == "comments-file":
                child.text = self.comments_file
            elif child.tag == "scene-order-file":
                child.text = self.scene_order_file
            elif child.tag == "topic-sort-by-name":
                child.text = self.topic_sort_by_name
            elif child.tag == "app-theme":
                child.text = self.app_theme
            elif child.tag == "csv-editor-cmd":
                child.text = self.csv_editor_cmd
            elif child.tag == "audio-wpm":
                child.text = str(self.audio_wpm)
            elif child.tag == "audio-word-len":
                child.text = str(self.audio_word_len)
            elif child.tag == "audio-min-time":
                child.text = str(self.audio_min_time)
            elif child.tag == "audio-padding":
                child.text = str(self.audio_padding)
        xml_bytes = ET.tostring(root, encoding='utf8', method='xml')
        with open(self.settings_file, "w") as f:
            f.write(xml_bytes.decode("utf-8"))

    def log_level(self):
        return {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARN": logging.WARN,
            "ERROR": logging.ERROR,
        }.get(self.log_level, logging.DEBUG)

    def topic_sort_by_name_ret(self):
        if self.topic_sort_by_name.upper() == "TRUE":
            return True
        else:
            return False

    def reset(self):
        self.skyrim_path = AppSettings.SKYRIM_PATH
        self.docgen_dir = AppSettings.DOGEN_DIR
        self.log_level = AppSettings.LOG_LEVEL
        self.actors_file = AppSettings.ACTORS_FILE
        self.comments_file = AppSettings.COMMENTS_FILE
        self.scene_order_file = AppSettings.SCENE_ORDER_FILE
        self.topic_sort_by_name = AppSettings.TOPIC_SORT_BY_NAME
        self.app_theme = AppSettings.DEFAULT_THEME
        self.csv_editor_cmd = AppSettings.CSV_EDITOR_CMD
        # audio settings
        self.audio_wpm = AppSettings.AUDIO_WPM
        self.audio_word_len = AppSettings.AUDIO_WORD_LEN
        self.audio_min_time = AppSettings.AUDIO_MIN_TIME
        self.audio_padding = AppSettings.AUDIO_PADDING

    def reset_and_save(self):
        self.reset()
        self.save()


if __name__ == '__main__':
    settings_file = "..\sandbox\settings\settings.text.xml"
    s = AppSettings(settings_file=settings_file)
    print("s.skyrim_path:", s.skyrim_path)
    print("s.app_theme:", s.app_theme)
    print("s.docgen_dir_json:", s.docgen_dir_json)
    s.skyrim_path = s.skyrim_path + "__"
    s.save()
