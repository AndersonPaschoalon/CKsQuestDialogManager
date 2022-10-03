import json
import os
import logging
from PyUtils.Obj2Json import Obj2Json


class AppSettings:
    """
    Store all configurable settings from the application.
    """
    SKYRIM_PATH = ".\\Sandbox\\"
    DOGEN_DIR = ".\\OUTPUT\\"
    ACTORS_FILE = ".\\Actors.csv"
    COMMENTS_FILE = ".\\Comments.csv"
    SCENE_ORDER_FILE = ".\\SceneOrder.csv"
    TOPIC_SORT_BY_NAME = "true"
    CMD_COMMENT = "Use \"Process\" string for multiprocessing import, otherwise will be executed as a batch command. Use {file} variable to pass the csv file full path. Any other command line application can be set as editor."
    DEFAULT_THEME = "DarkBlue12"
    AUDIO_WPM = 110
    AUDIO_WORD_LEN = 5
    AUDIO_MIN_TIME = 2
    AUDIO_PADDING = 1

    def __init__(self, json_file):
        self.settings_file = json_file
        with open(json_file) as f:
            self.data = json.load(f)
        self.skyrim_path = self.data["skyrim-path"]
        self.docgen_dir = os.path.abspath(self.data["dogen-dir"])
        self.log_level = self.data["log-level"]
        self.actors_file = self.data["actors-file"]
        self.comments_file = self.data["comments-file"]
        self.scene_order_file = self.data["scene-order-file"]
        self.topic_sort_by_name = self.data["topic-sort-by-name"]
        self.app_theme = self.data["app-theme"]
        self.csv_editor_cmd_comments = self.data["csv-editor-cmd-comments"]
        self.csv_editor_cmd = self.data["csv-editor-cmd"]
        self.audio_wpm = int(self.data["audio-wpm"])
        self.audio_word_len = int(self.data["audio-word-len"])
        self.audio_min_time = int(self.data["audio-min-time"])
        self.audio_padding = int(self.data["audio-padding"])
        # derivated settings
        self.docgen_dir_md = self.docgen_dir + "\\Md\\"
        self.docgen_dir_json = self.docgen_dir + "\\Json\\"
        self.docgen_dir_html = self.docgen_dir + "\\Html\\"
        self.docgen_dir_docx = self.docgen_dir + "\\Docx\\"
        self.docgen_reports = self.docgen_dir + "\\Reports\\"

    def save(self):
        self.data["skyrim-path"] = self.skyrim_path
        self.data["dogen-dir"] = self.docgen_dir
        self.data["log-level"] = self.log_level
        self.data["actors-file"] = self.actors_file
        self.data["comments-file"] = self.comments_file
        self.data["scene-order-file"] = self.scene_order_file
        self.data["topic-sort-by-name"] = self.topic_sort_by_name
        self.data["app-theme"] = self.app_theme
        self.data["csv-editor-cmd"] = self.csv_editor_cmd
        self.data["audio-wpm"] = str(self.audio_wpm)
        self.data["audio-word-len"] = str(self.audio_word_len)
        self.data["audio-min-time"] = str(self.audio_min_time)
        self.data["audio-padding"] = str(self.audio_padding)
        with open(self.settings_file, "w") as a_file:
            json.dump(self.data, a_file, indent=4)

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
        self.actors_file = AppSettings.ACTORS_FILE
        self.comments_file = AppSettings.COMMENTS_FILE
        self.scene_order_file = AppSettings.SCENE_ORDER_FILE
        self.topic_sort_by_name = AppSettings.TOPIC_SORT_BY_NAME
        self.app_theme = AppSettings.DEFAULT_THEME
        # audio settings
        self.audio_wpm = AppSettings.AUDIO_WPM
        self.audio_word_len = AppSettings.AUDIO_WORD_LEN
        self.audio_min_time = AppSettings.AUDIO_MIN_TIME
        self.audio_padding = AppSettings.AUDIO_PADDING

    def reset_and_save(self):
        self.reset()
        self.save()
