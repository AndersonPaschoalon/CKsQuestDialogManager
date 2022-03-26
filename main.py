# This is a sample Python script.
import logging
from QuestExports.QuestDialogs import QuestDialogs
from PyUtils.Logger import Logger
from PyUtils.Console import Console
from Gui.MainWindow import MainWindow
from Gui.AudioWindow import AudioWindow


LOG_FILE = "./App/Logs/ck-dialog-docgen.log"
DOC_OUTPUT = "./OUTPUT/"

def test_build_quest_objs():
    Logger.initialize(LOG_FILE, level_log=logging.DEBUG, level_console=logging.WARNING)
    QuestDialogs.generate_quest_documentation("./Sandbox/", "./Comments.csv", "./Actors.csv",
                                              "./SceneOrder.csv", DOC_OUTPUT)

def test_export_objs():
    skyrim_path = "./Sandbox/"
    comments_csv = "Comments.csv"
    actors_csv = "Actors.csv"
    QuestDialogs.export_objects_to_csvdics(skyrim_path, comments_csv, actors_csv)

def test_run_audio_window():
    audio_win = AudioWindow()
    audio_win.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #test_build_quest_objs()
    app = MainWindow()
    app.run()

