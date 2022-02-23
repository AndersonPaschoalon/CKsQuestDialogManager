# This is a sample Python script.
from QuestExports.QuestDialogs import QuestDialogs
from PyUtils.Console import Console

def test_build_quest_objs():
    QuestDialogs.build_quest_objects("./Sandbox/")

def test_export_objs():
    skyrim_path = "./Sandbox/"
    comments_csv = "Comments.csv"
    actors_csv = "Actors.csv"
    QuestDialogs.export_objects_to_csvdics(skyrim_path, comments_csv, actors_csv)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # test_build_quest_objs()
    test_export_objs()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
