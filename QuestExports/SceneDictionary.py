import csv
from os import listdir
from os.path import isfile, join
from PyUtils.Cd import Cd
from PyUtils.Logger import Logger
from PyUtils.Obj2Json import Obj2Json
from PyUtils.Functions import *
from QuestExports.Consts import Consts


class SceneDictionary:
    """
    This class must stores the entries imported from SceneDialog exports, one entry by unique row for
    each quest.
    """
    """
    # CSV keys
    LABEL_SCENE_SCENE = 'SCENE'
    LABEL_SCENE_ALIAS = 'ALIAS'
    LABEL_SCENE_VOICE_TYPE = 'VOICE TYPE'
    LABEL_SCENE_FILENAME = 'FILENAME'
    LABEL_SCENE_RESPONSE_TEXT = 'RESPONSE TEXT'
    LABEL_SCENE_SUPPORTING_DIALOGUE = 'SUPPORTING DIALOGUE'
    LABEL_SCENE_EMOTION = 'EMOTION'
    LABEL_SCENE_SCRIPT_NOTES = 'SCRIPT NOTES'
    LABEL_SCENE_SCENE_PHASE = 'SCENE PHASE'
    # Scene files
    SCENE_PREFIX = 'SceneDialogue_'
    SCENE_SUFIX = '.txt'
    """

    def __init__(self):
        """
        Constructor
        """
        self.scene_id = ""  # SceneDialogue.SCENE
        self.alias = ""  # SceneDialogue.ALIAS
        self.voice_type = ""  # SceneDialogue.VOICE TYPE
        self.filename = ""  # SceneDialogue.FILENAME (key)
        self.dialogue = ""  # SceneDialogue.RESPONSE TEXT	SUPPORTING DIALOGUE
        self.emotion = ""  # SceneDialogue.EMOTION
        self.notes = ""  # SceneDialogue.SCRIPT NOTES
        self.scene_phase = -1  # SceneDialogue.SCENE PHASE (last)
        self._log = Logger.get()

    def to_string(self):
        obj = Obj2Json()
        obj.add()
        obj.add("scene_id", self.scene_id)
        obj.add("alias", self.alias)
        obj.add("voice_type", self.voice_type)
        obj.add("filename", self.filename)
        obj.add("dialogue", self.dialogue)
        obj.add("emotion", self.emotion)
        obj.add("notes", self.notes)
        obj.add("scene_phase", self.scene_phase)
        return obj.json()

    @staticmethod
    def build_scene_dictionary(skyrim_path: str, quest_id: str):
        """
        Build a scene dictionary to easy and pre-process the exported data from Scenes.
        :param skyrim_path:
        :param quest_id:
        :return:
        """
        _log = Logger.get()
        _log.debug("SceneDictionary.build_scene_dictionary() skyrim_path:" + skyrim_path + ", quest_id:" + quest_id)
        export_dialog_files = SceneDictionary.list_scene_files(skyrim_path, quest_id)
        list_scenes_dics = []
        with Cd(skyrim_path):
            for nth_file in export_dialog_files:
                _log.info("-- processing file " + nth_file)
                print("-- processing file " + nth_file)
                if is_non_zero_file(nth_file):
                    with open(nth_file) as fd:
                        rd = csv.reader(fd, delimiter="\t", quotechar='"')
                        # calc the positions for each file
                        first_row = next(rd)
                        col_scene = SceneDictionary._get_index(first_row, Consts.LABEL_SCENE_SCENE)
                        col_alias = SceneDictionary._get_index(first_row, Consts.LABEL_SCENE_ALIAS)
                        col_voice = SceneDictionary._get_index(first_row, Consts.LABEL_SCENE_VOICE_TYPE)
                        col_file = SceneDictionary._get_index(first_row, Consts.LABEL_SCENE_FILENAME)
                        col_response = SceneDictionary._get_index(first_row, Consts.LABEL_SCENE_RESPONSE_TEXT)
                        col_supporting = SceneDictionary._get_index(first_row, Consts.LABEL_SCENE_SUPPORTING_DIALOGUE)
                        col_emotion = SceneDictionary._get_index(first_row, Consts.LABEL_SCENE_EMOTION)
                        col_notes = SceneDictionary._get_index(first_row, Consts.LABEL_SCENE_SCRIPT_NOTES)
                        col_phase = SceneDictionary._get_index(first_row, Consts.LABEL_SCENE_SCENE_PHASE)
                        for row in rd:
                            sd = SceneDictionary()
                            sd.scene_id = row[col_scene]
                            sd.alias = row[col_alias]
                            sd.voice_type = row[col_voice]
                            sd.filename = row[col_file]
                            sd.emotion = row[col_emotion]
                            sd.notes = row[col_notes]
                            sd.scene_phase = int(row[col_phase])
                            response = row[col_response].strip()
                            supporting = row[col_supporting].strip()
                            diag_text = ""
                            if response == "":
                                diag_text = supporting
                            else:
                                diag_text = response
                            sd.dialogue = diag_text
                            if not any(x.filename == sd.filename for x in list_scenes_dics):
                                list_scenes_dics.append(sd)
                            else:
                                _log.debug("** Dic already have entry x.filename:" + sd.filename + " (" + nth_file + ")")
                else:
                    _log.warn("**WARN** " + nth_file + " IS EMPTY.")
        _log.debug("build_scene_dictionary()")
        return list_scenes_dics

    @staticmethod
    def list_scene_files(skyrim_path: str, quest_id: str):
        _log = Logger.get()
        _log.debug("SceneDictionary.list_scene_files()")
        all_files = [f for f in listdir(skyrim_path) if isfile(join(skyrim_path, f))]
        # filter all exported files from creation kit
        export_dialog_files = []
        for nth_file in all_files:
            if (nth_file.startswith(Consts.EXPORT_SCENE_PREFIX) and
                    (nth_file.endswith(Consts.EXPORT_SCENE_EXT)) and
                    (quest_id in nth_file)):
                export_dialog_files.append(nth_file)
        _log.debug("export_dialog_files: " + str(export_dialog_files))
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

    @staticmethod
    def _is_non_zero_file(fpath: str):
        return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

if __name__ == '__main__':
    lsd = []
    lsd = SceneDictionary.build_scene_dictionary("..\\Sandbox\\", "DSilHand_M80AssaultJor")
    for sd in lsd:
        print("<" + sd.filename + ">")
