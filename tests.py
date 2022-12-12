import logging
from QuestExports.QuestDialogs import QuestDialogs
from PyUtils.Logger import Logger
from PyUtils.Console import Console
from Gui.MainWindow import MainWindow
from Gui.AudioWindow import AudioWindow
from Gui.AudioLogicLayer import AudioLogicLayer
from Settings.ProfileManager import ProfileManager


LOG_FILE = "./App/Logs/ck-dialog-docgen.log"
DOC_OUTPUT = "./OUTPUT/"


def test_build_quest_objs():
    Logger.initialize(LOG_FILE, level_log=logging.DEBUG, level_console=logging.WARNING)
    QuestDialogs.generate_quest_documentation("./Sandbox/", "./Comments.csv", "./Actors.csv",
                                              "./SceneOrder.csv", DOC_OUTPUT)

def test_export_objs():
    Logger.initialize(LOG_FILE, level_log=logging.DEBUG, level_console=logging.WARNING)
    skyrim_path = "./Sandbox/"
    comments_csv = "Comments.csv"
    actors_csv = "Actors.csv"
    QuestDialogs.export_objects_to_csvdics(skyrim_path, comments_csv, actors_csv)

def test_run_audio_window():
    Logger.initialize(LOG_FILE, level_log=logging.DEBUG, level_console=logging.WARNING)
    audio_win = AudioWindow()
    audio_win.run()

def test_audio_logic_layer_enerate_list_audio_data():
    audll = AudioLogicLayer(".\\App\\")
    list_audio_data = audll.generate_list_audio_data()
    print("==============================================")
    for ad in list_audio_data:
        print(ad.to_string())

def test_audio_window():
    audio_win = AudioWindow("App\\")
    audio_win.run()


def calc_reading_time(text, wpm=110, word_len=5, min_time=2, padding=0):
    # split text in words
    text_list = text.split()
    # count words
    total_words = 0
    for current_text in text_list:
        total_words += len(current_text)/word_len
    # calc reading time in seconds
    read_time = (total_words*60)/wpm
    # add padding
    read_time = read_time + padding
    # ensure min time
    read_time = max([read_time, min_time])
    return round(read_time)


def speech_time_test():
    phrase = "My life had gained a new purpose. I Joined the Silver Hands and I'm helping with the forge since then."
    print("calc_reading_time:", calc_reading_time(phrase))

def test_profile_manager():
    print("")
    pm = ProfileManager()
    ret, list_profiles, msg = pm.get_profile_list()
    if not ret:
        print("Error: ", msg)
        return False
    for item in list_profiles:
        print(" - item.name:", item.name, ", item.comments:", item.comment)
    # create new profile
    # pm.create_profile(profile_name="TestProfile01", comment="First test profile. This is a comment.")
    # create new profile
    # pm.create_profile(profile_name="TestProfile02", comment="Second test profile. This is a comment.")
    # create new profile
    # activate profile
    pm.activate_profile(new_active_profile="TestProfile02")
    # delete profile
    # activate profile
    # create profile


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bool_test_audio_logic_layer_enerate_list_audio_data = False
    bool_test_audio_window = False
    bool_test_speach_time = False
    bool_test_profile = True
    if bool_test_audio_logic_layer_enerate_list_audio_data:
        test_audio_logic_layer_enerate_list_audio_data()
    if bool_test_audio_window:
        test_audio_window()
    if bool_test_speach_time:
        speech_time_test()
    if bool_test_profile:
        test_profile_manager()
