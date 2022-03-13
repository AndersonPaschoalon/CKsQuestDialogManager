import csv
import os
from os import listdir
from os.path import isfile, join
from PyUtils.Cd import Cd
from PyUtils.Obj2Json import Obj2Json
from QuestExports.SceneDictionary import SceneDictionary
from QuestExports.DialogLine import DialogLine
from QuestExports.SceneTopic import SceneTopic

class Scene:

    EXPORT_DIALOG_PREFIX = "dialogueExport"
    EXPORT_DIALOG_EXT = ".txt"
    EXPORT_FULL_PATH = 'FULL PATH'
    EXPORT_FILENAME = 'FILENAME'
    EXPORT_RESPONSE_INDEX = 'RESPONSE INDEX'
    EXPORT_CATEGORY = 'CATEGORY'
    EXPORT_SCENE_VAL = "Scene"

    def __init__(self, quest_id: str, scene_id: str):
        self.quest_id = ""
        self.scene_id = ""
        self.list_scene_topics = []

    def to_string(self):
        print("oi")

    def set_scene_topics(self, list_scenes_topics: list):
        self.list_scene_topics = list_scenes_topics

    def set_dialog_export(self, filename_key: str, response_index: int, filepath: str):
        i = 0
        was_set = False
        while i < len(self.list_scene_topics):
            list_keys = self.list_scene_topics[i].get_list_filenames_keys()
            if filename_key in list_keys:
                # set_dialog_export(self, filename_key: str, response_index: int, filepath: str)
                self.list_scene_topics[i].set_dialog_export(filename_key, response_index, filepath)
            i += 1

    def get_list_filenames_keys(self):
        i = 0
        list_filenames = []
        for dl in self.list_scene_topics:
            list_scene_keys = dl.get_list_filenames_keys()
            for key in list_scene_keys:
                list_filenames.append(key)
        return list_filenames

    def sort_scenes(self):
        i = 0
        while i < len(self.list_scene_topics):
            self.list_scene_topics[i].sort_dialog_lines()
            i += 1
        # TODO: SORT SCENES ID BY NAME

    @staticmethod
    def list_scene_quests(skyrim_path: str):
        print("oi")

    @staticmethod
    def build_scenes_list(skyrim_path: str, quest_id: str):
        """
        skyrim_path -> "..\Sandbox\\"
        quest_id -> "DSilHand_M80AssaultJor"
        :param skyrim_path:
        :param quest_id:
        :return:
        """
        # (1) Create the list of scenes using the SceneDialog files
        list_scenes = []
        list_scene_topics = []
        list_dialog_lines = []
        lsd = SceneDictionary.build_scene_dictionary(skyrim_path, quest_id)
        last_scene_id = ""
        last_phase = -1
        last_alias = ""
        last_voice_type = ""
        for item in lsd:
            dl = DialogLine()
            dl.set_scene_dialog(item.filename, item.dialogue, item.emotion, item.notes)
            # we are in the same scene, so we keep accumulating the dialogues lines to the same topic object
            if last_scene_id == item.scene_id or last_scene_id == "":
                # if it is the same phase or the first, just append
                if item.scene_phase == last_phase or last_phase == -1:
                    # add to the acc list of dialog lines
                    list_dialog_lines.append(dl)
                else:
                    # it is a new phase, create the SceneTopic, add the current list, clear it and creates a new
                    # line entry
                    st = SceneTopic(last_scene_id, last_alias, last_voice_type, last_phase)
                    st.sd_list_dialog_lines = list_dialog_lines
                    list_scene_topics.append(st)
                    list_dialog_lines.clear()
                    list_dialog_lines.append(dl)
            # we are not in the same scene anymore. Therefore we need to add the created list to a new
            # Scene object.
            else:
                scene = Scene(quest_id, last_scene_id)
                scene.set_scene_topics(list_scene_topics)
                list_scene_topics.clear()
                list_scenes.append(scene)
            # update "last_" variables with the current itens
            last_scene_id = item.scene_id
            last_phase = item.scene_phase
            last_alias = item.alias
            last_voice_type = item.voice_type
        # (2) Update the list of scenes using data from dialogExport_
        quest_ex_file = Scene._get_quest_exported(skyrim_path, quest_id)
        with Cd(skyrim_path):
            with open(quest_ex_file) as fd:
                rd = csv.reader(fd, delimiter="\t", quotechar='"')
                # calc the positions for each file
                first_row = next(rd)
                col_fullpath = Scene._get_index(first_row, Scene.EXPORT_FULL_PATH)
                col_filename = Scene._get_index(first_row, Scene.EXPORT_FILENAME)
                col_res_index = Scene._get_index(first_row, Scene.EXPORT_RESPONSE_INDEX)
                col_category = Scene._get_index(first_row, Scene. EXPORT_CATEGORY)
                col_file = Scene._get_index(first_row, Scene.EXPORT_FILEPATH)
                for row in rd:
                    fullpath = row[col_fullpath]
                    filename = row[col_filename]
                    res_index = row[col_res_index]
                    category = row[col_category]
                    if category == Scene.EXPORT_SCENE_VAL:
                        list_scenes = Scene._update_dialogexport_scenelist(list_scenes, filename, res_index, fullpath)
        print("")
        i = 0
        while i < len(list_scenes):
            list_scenes[i].sort_scenes()
            i += 1

    @staticmethod
    def _update_dialogexport_scenelist(list_scenes: list, filename_key: str, response_index: int, filepath: str):
        print("")
        i = 0
        while i < len(list_scenes):
            list_keys = list_scenes[i].get_list_filenames_keys
            if filename_key in list_keys:
                list_scenes[i].set_dialog_export(filename_key, response_index, filepath)
            i += 1
        return list_scenes

    @staticmethod
    def _get_quest_exported(skyrim_path: str, quest_id: str):
        list_all_exported = SceneTopic._get_all_export_dialog_files(skyrim_path)
        for ex in list_all_exported:
            if quest_id in ex:
                return ex
        return ""

    @staticmethod
    def _get_all_export_dialog_files(skyrim_path: str):
        """
        Return all the expoted dialog files names inside Skyrim root directory.
        :param skyrim_path: The skyrim root directory.
        :return: list of expoted dialog files.
        """
        all_files = [f for f in listdir(skyrim_path) if isfile(join(skyrim_path, f))]
        # filter all exported files from creation kit
        export_dialog_files = []
        for nth_file in all_files:
            if (nth_file.startswith(DialogLine.EXPORT_DIALOG_PREFIX) and
                    nth_file.endswith(DialogLine.EXPORT_DIALOG_EXT)):
                export_dialog_files.append(nth_file)
        return export_dialog_files

    @staticmethod
    def _get_index(first_row, label):
        """
        Tells the position of a given label in a CSV line.
        :param first_row: The first row of a CSV file.
        :param label: The label of the CSV file whose the position must be known.
        :return:
        """
        if len(first_row) == 0:
            return 0
        return first_row.index(label)


if __name__ == '__main__':
    Scene.build_scenes_list("..\Sandbox\\", "DSilHand_M80AssaultJor")

