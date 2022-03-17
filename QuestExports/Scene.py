import csv
import os
from typing import List
from os import listdir
from os.path import isfile, join
from PyUtils.Cd import Cd
from PyUtils.Obj2Json import Obj2Json
from PyUtils.CsvDicTuple import CsvDicTuple
from PyUtils.CsvDic import CsvDic
from PyUtils.Logger import Logger
from PyUtils.Functions import *
from QuestExports.SceneDictionary import SceneDictionary
from QuestExports.DialogLine import DialogLine
from QuestExports.SceneTopic import SceneTopic
from QuestExports.Consts import Consts



class Scene:
    """
    Store information of a Scene.
    A Scene is a sequence of dialoges of many charactes organized in a structured
    way in a Scene object of creation Kit.
    A scene is composed of an ordered sequence of SceneTopics.
    """
    """
    EXPORT_SCENE_PREFIX = 'SceneDialogue_'
    EXPORT_SCENE_EXT = '.txt'
    EXPORT_DIALOG_PREFIX = "dialogueExport"
    EXPORT_DIALOG_EXT = ".txt"
    LABEL_SCENE_FULL_PATH = 'FULL PATH'
    LABEL_SCENE_FILENAME = 'FILENAME'
    LABEL_SCENE_QUEST = 'QUEST'
    LABEL_SCENE_SCENE = 'SCENE'
    LABEL_SCENE_RESPONSE_INDEX = 'RESPONSE INDEX'
    LABEL_SCENE_CATEGORY = 'CATEGORY'
    STR_SCENE_VAL = "Scene"
    """

    def __init__(self, quest_id: str, scene_id: str):
        """
        Constructor.
        :param quest_id: quest ID for the scene.
        :param scene_id: scene ID.
        """
        self.quest_id = quest_id
        self.scene_id = scene_id
        self.scene_position = -1
        self.comment = ""
        self.list_scene_topics = []
        self._log = Logger.get()

    def to_string(self):
        """
        Build a Json string representation of the object.
        :return: json string.
        """
        self._log.debug("Scene.to_string()")
        obj = Obj2Json()
        obj.add("quest_id", self.quest_id)
        obj.add("scene_id", self.scene_id)
        obj.add("scene_position", self.scene_position)
        obj.add("comment", self.comment)
        list_scene_topics_str = []
        for st in self.list_scene_topics:
            list_scene_topics_str.append(st.to_string())
        obj.addl("list_scene_topics", list_scene_topics_str)
        return obj.json()

    def count_dialog_lines(self):
        acc_dialog_lines = 0
        for st in self.list_scene_topics:
            acc_dialog_lines += st.count_dialog_lines()
        return acc_dialog_lines

    def is_empty(self):
        """
        Tells of the scene object is empty or not.
        :return: True if it is empty, False otherwise.
        """
        cc = self.count_dialog_lines()
        if cc == 0:
            return True
        else:
            return False

    def set_scene_topics(self, list_scenes_topics: List[SceneTopic]):
        """
        Update the list of Scene Topics for the Scene.
        :param list_scenes_topics: list of SceneTopics.
        :return: void
        """
        self._log.debug("Scene.set_scene_topics() len(list_scenes_topics): " + str(len(list_scenes_topics)))
        self.list_scene_topics.clear()
        for st in list_scenes_topics:
            self.list_scene_topics.append(st)

    def set_dialog_export(self, filename_key: str, response_index: int, filepath: str,
                          actor_id: str, actor_race: str, dialog_type: str):
        """
        Set data from dialogExport using the filename as key. It search for the filename_key in the list
        of scene topics, in order to find which SceneTopic must be updated.
        :param filename_key: 'FILENAME' column in the SceneDialog_ and dialogExport file.
        :param response_index: 'RESPONSE INDEX' column.
        :param filepath:  'FULL PATH' column.
        :param actor_id: 'NPCID' column.
        :param actor_race: 'RACE' column
        :param dialog_type: 'CATEGORY' column.
        :return: void.
        """
        self._log.debug("Scene.set_dialog_export() filename_key:" + filename_key + ", response_index:" + response_index
                        + ", filepath:" + filepath + ", actor_id:" + actor_id + ", actor_race:" + actor_race +
                        ", dialog_type:" + dialog_type)
        i = 0
        while i < len(self.list_scene_topics):
            list_keys = self.list_scene_topics[i].get_list_filenames_keys()
            if filename_key in list_keys:
                self.list_scene_topics[i].set_dialog_export(filename_key, response_index, filepath,
                                                            actor_id, actor_race, dialog_type)
            i += 1

    def get_list_filenames_keys(self):
        """
        Returns the list of FILENAME entries from this Scene -- which is used as key for each dialog line.
        :return: list of FILENAME entries.
        """
        list_filenames = []
        self._log.debug("get_list_filenames_keys()")
        self._log.debug("len(self.list_scene_topics):" + str(len(self.list_scene_topics)) +\
                        "for quest:" + self.quest_id + ", scene:" + self.scene_id )
        if len(self.list_scene_topics) > 0:
            for st in self.list_scene_topics:
                list_scene_keys = st.get_list_filenames_keys()
                for key in list_scene_keys:
                    list_filenames.append(key)
        self._log.debug("quest:" + self.quest_id + ", scene:" + self.scene_id + " > " + str(list_filenames))
        return list_filenames

    def sort_scenes_topics(self):
        """
        Sort the scene topics, and all the list beneath it.
        :return: void
        """
        self._log.debug("sort_scenes_topics()")
        i = 0
        # sort dialog lines
        while i < len(self.list_scene_topics):
            self.list_scene_topics[i].sort_dialog_lines()
            i += 1
        # sort scene phases
        self.list_scene_topics.sort(key=lambda x: x.get_scene_phase(), reverse=False)
        self._log.debug("elements from self.list_scene_topics sorted for quest " + self.quest_id + ", scene " +\
                        self.scene_id)

    def set_position(self, position: int):
        """
        Set the position of the Scene relative to the quest.
        :param position: position from 0 to n.
        :return: void
        """
        self._log.debug("Setting position " + str(position) + "for scene " + self.scene_id + " in the quest " +\
                        self.quest_id)
        self.scene_position = position

    def get_position(self):
        """
        Return the position self.scene_position.
        :return: void
        """
        return self.scene_position

    @staticmethod
    def list_scene_quests(skyrim_path: str):
        """
        This method list all the quests with exported scenes from skyrim directory.
        :param skyrim_path: path where the SceneDialog_ files are going to be searched.
        :return: list of quest IDs with exported scenes.
        """
        _log = Logger.get()
        _log.debug("Scene.list_scene_quests()")
        all_files = [f for f in listdir(skyrim_path) if isfile(join(skyrim_path, f))]
        all_diag_export_quests = []
        scene_quests = []
        for f in all_files:
            if f.startswith(Consts.EXPORT_DIALOG_PREFIX) and f.endswith(Consts.EXPORT_DIALOG_EXT):
                quest_id = f.replace(Consts.EXPORT_DIALOG_PREFIX, "").replace(Consts.EXPORT_DIALOG_EXT, "")
                all_diag_export_quests.append(quest_id)
        for f in all_files:
            if f.startswith(Consts.EXPORT_SCENE_PREFIX) and f.endswith(Consts.EXPORT_SCENE_EXT):
                for g in all_diag_export_quests:
                    if g in f:
                        scene_quests.append(g)
                        break
        scene_quests = list(dict.fromkeys(scene_quests))
        _log.debug("scene_quests: " + str(scene_quests))
        return scene_quests

    @staticmethod
    def export_scenes_to_csvdic(skyrim_path: str, csv_dic_order: str, csv_dic_comemnts: str, csv__dic_actors):
        """
        Export Quests IDs and Scenes IDs to SceneOrder.csv.
        :param skyrim_path: Skyrim path where the Scenes files are going to be searched.
        :param csv_dic_order: The CSV SceneOrder dictionary.
        :return: [all_scene_files, quest_scenes_no_duplicates]: returns a list of exported Scenes files exported,
        and an array of tuples (QuestID, SceneIDs).
        """
        _log = Logger.get()
        _log.debug("Scene.export_scenes_to_csvdic() skyrim_path:" + skyrim_path + ", csv_dic:" + csv_dic_order)
        all_scene_files = []
        all_files = [f for f in listdir(skyrim_path) if isfile(join(skyrim_path, f))]
        for f in all_files:
            if f.startswith(Consts.EXPORT_SCENE_PREFIX) and f.endswith(Consts.EXPORT_SCENE_EXT):
                all_scene_files.append(f)
        list_quest_scenes_pairs = []
        list_scenes = []
        list_alias = []
        with Cd(skyrim_path):
            for f in all_scene_files:
                print("openning file " + f)
                if is_non_zero_file(f):
                    with open(f) as fd:
                        rd = csv.reader(fd, delimiter=Consts.EXPORT_SCENE_DELIMITER, quotechar='"')
                        first_row = next(rd)
                        col_quest = Scene._get_index(first_row, Consts.LABEL_SCENE_QUEST)
                        col_scene = Scene._get_index(first_row, Consts.LABEL_SCENE_SCENE)
                        col_alias = Scene._get_index(first_row, Consts.LABEL_SCENE_ALIAS)
                        for row in rd:
                            list_quest_scenes_pairs.append((row[col_quest], row[col_scene]))
                            list_scenes.append(row[col_scene])
                            list_alias.append(row[col_alias])
                else:
                    _log.warn("**WARN**  FILE " + f + " is empty")
        # remove duplicates from pairs
        quest_scenes_no_duplicates = []
        for qs in list_quest_scenes_pairs:
            if qs not in quest_scenes_no_duplicates:
                quest_scenes_no_duplicates.append(qs)
        # remove duplicates from scene list
        list_scenes = list(dict.fromkeys(list_scenes))
        list_alias = list(dict.fromkeys(list_alias))
        # add to SceneOrder dic
        scene_tuple = CsvDicTuple(csv_dic_order)
        for qs in quest_scenes_no_duplicates:
            print(" -- qs: " + qs[0] + ", " + qs[1])
            scene_tuple.add_tuple(qs[0], qs[1])
        # add to Comments csv
        comments = CsvDic(csv_dic_comemnts)
        for scene in list_scenes:
            comments.add(scene, "")
        # add aliases to Actors csv
        actors = CsvDic(csv__dic_actors)
        for al in list_alias:
            actors.add(al)
        _log.debug("all_scene_files:" + str(all_scene_files))
        _log.debug("quest_scenes_no_duplicates:" + str(quest_scenes_no_duplicates))
        return [all_scene_files, quest_scenes_no_duplicates, list_scenes]

    @staticmethod
    def build_scenes_list(skyrim_path: str, quest_id: str, scene_order_dic: str, comments_csv: str, actors_csv: str):
        """
        Build the Scene data structure. Each quest contains n Scenes. Each Scene
        skyrim_path -> "..\\Sandbox\\"
        quest_id -> "DSilHand_M80AssaultJor"
        :param skyrim_path: -> "..\\Sandbox\\"
        :param quest_id: -> "DSilHand_M80AssaultJor"
        :param scene_order_dic:
        :param comments_csv:
        :param actors_csv:
        :return:  list of crafted scenes objects.
        """
        _log = Logger.get()
        _log.debug("build_scenes_list() skyrim_path:" + skyrim_path + ", quest_id:" + quest_id)
        _log.debug("Create the list of scenes using the SceneDialog files...")
        # (1) Create the list of scenes using the SceneDialog files
        list_scenes = []
        list_scene_topics = []
        list_dialog_lines = []
        # each unique dialog entry for the quest
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
                    st.set_dialog_lines(list_dialog_lines)
                    list_scene_topics.append(st)
                    list_dialog_lines.clear()
                    list_dialog_lines.append(dl)
            # we are not in the same scene anymore. Therefore we need to add the created list to a new
            # Scene object.
            else:
                # creates and appends the last scene topic
                st = SceneTopic(last_scene_id, last_alias, last_voice_type, last_phase)
                st.set_dialog_lines(list_dialog_lines)
                list_scene_topics.append(st)
                list_dialog_lines.clear()
                list_dialog_lines.append(dl)
                scene = Scene(quest_id, last_scene_id)
                scene.set_scene_topics(list_scene_topics)
                list_scene_topics.clear()
                list_scenes.append(scene)
            # update "last_" variables with the current itens
            last_scene_id = item.scene_id
            last_phase = item.scene_phase
            last_alias = item.alias
            last_voice_type = item.voice_type
        # create last scene topic
        st = SceneTopic(last_scene_id, last_alias, last_voice_type, last_phase)
        st.set_dialog_lines(list_dialog_lines)
        list_dialog_lines.clear()
        list_scene_topics.append(st)
        # add the last scene
        scene = Scene(quest_id, last_scene_id)
        scene.set_scene_topics(list_scene_topics)
        list_scene_topics.clear()
        list_scenes.append(scene)
        _log.debug("Update the list of scenes using data from dialogExport_...")
        # (2) Update the list of scenes using data from dialogExport_
        quest_ex_file = Scene._get_quest_exported(skyrim_path, quest_id)
        with Cd(skyrim_path):
            with open(quest_ex_file) as fd:
                rd = csv.reader(fd, delimiter="\t", quotechar='"')
                # calc the positions for each file
                first_row = next(rd)
                #col_fullpath = Scene._get_index(first_row, Consts.LABEL_SCENE_FULL_PATH)
                #col_filename = Scene._get_index(first_row, Consts.LABEL_SCENE_FILENAME)
                #col_res_index = Scene._get_index(first_row, Consts.LABEL_SCENE_RESPONSE_INDEX)
                #col_category = Scene._get_index(first_row, Consts. LABEL_SCENE_CATEGORY)
                col_fullpath = Scene._get_index(first_row, Consts.LABEL_DIALOG_FULL_PATH)
                col_filename = Scene._get_index(first_row, Consts.LABEL_DIALOG_FILENAME)
                col_res_index = Scene._get_index(first_row, Consts.LABEL_DIALOG_NPC_RESPONSE_INDEX)
                col_category = Scene._get_index(first_row, Consts.LABEL_DIALOG_CATEGORY)
                col_actor_id = Scene._get_index(first_row, Consts.LABEL_DIALOG_NPC_SPEAKER)
                col_actor_race = Scene._get_index(first_row, Consts.LABEL_DIALOG_NPC_RACE)
                for row in rd:
                    fullpath = row[col_fullpath]
                    filename = row[col_filename]
                    res_index = row[col_res_index]
                    category = row[col_category]
                    actor_id = row[col_actor_id]
                    actor_race = row[col_actor_race]
                    if category == Consts.STR_SCENE_VAL:
                        list_scenes = Scene._update_dialogexport_scenelist(list_scenes, filename, res_index, fullpath,
                                                                           actor_id, actor_race, category)
        # (3) sort scenes
        _log.debug("sorting scenes...")
        i = 0
        _log.debug("scene_order_dic:" + scene_order_dic)
        scene_order = CsvDicTuple(scene_order_dic)
        while i < len(list_scenes):
            scene_pos = scene_order.tuple_position(list_scenes[i].quest_id, list_scenes[i].scene_id)
            list_scenes[i].sort_scenes_topics()
            list_scenes[i].set_position(scene_pos)
            i += 1
        list_scenes.sort(key=lambda x: x.get_position(), reverse=False)
        _log.debug("build_scenes_list() completed")
        # (4) Update Comments and Actor names
        _log.debug("instantiate Actors and Comments dictionary")
        comments = CsvDic(comments_csv, Consts.CSV_COMMENTS_DELIMITER)
        actors_dic = CsvDic(actors_csv, Consts.CSV_ACTOR_DELIMITER)
        i = 0
        for sc in list_scenes:
            _log.debug("Adding comment for " + sc.scene_id)
            sc.comment = comments.get(sc.scene_id, Consts.DEFAULT_SCENE_DESCRIPTION)
            while i < len(sc.list_scene_topics):
                act_id = sc.list_scene_topics[i].get_actor_id()
                # if it is an ampty actor ID, try to search for alias
                if act_id == Consts.STR_EMPTY_ACTOR_ID:
                    act_id = sc.list_scene_topics[i].get_actor_alias()
                name = actors_dic.get(act_id, act_id)
                print("act_id:" + act_id + ", name:" + name)
                sc.list_scene_topics[i].set_actor_name(name)
                i += 1
            i = 0
        # print results
        print("** Results **")
        for ss in list_scenes:
            print(ss.to_string())
            n_diag_lines = ss.count_dialog_lines()
            # print("n_diag_lines:" + str(n_diag_lines))
        return list_scenes

    # private methods

    @staticmethod
    def _update_dialogexport_scenelist(list_scenes: list, filename_key: str, response_index: int, filepath: str,
                                       actor_id: str, actor_race: str, dialog_type: str):
        """
        Updates the list of Scene objects with the data from dialogExport files, executing the method
        set_dialog_export() for each element.
        :param list_scenes:
        :param filename_key:
        :param response_index:
        :param filepath:
        :param actor_id:
        :param actor_race:
        :param dialog_type:
        :return:
        """
        _log = Logger.get()
        _log.debug("_update_dialogexport_scenelist()")
        i = 0
        while i < len(list_scenes):
            list_keys = list_scenes[i].get_list_filenames_keys()
            if filename_key in list_keys:
                list_scenes[i].set_dialog_export(filename_key, response_index, filepath,
                                                 actor_id, actor_race, dialog_type)
            i += 1
        return list_scenes

    @staticmethod
    def _get_quest_exported(skyrim_path: str, quest_id: str):
        """
        Returns the name of the dialogExport_ for a given quest ID.
        :param skyrim_path: directory where the dialogExport files are going to be searched.
        :param quest_id: the quest ID.
        :return: the name of the dialogExport file for a given quest ID.
        """
        _log = Logger.get()
        _log.debug("_get_quest_exported()")
        list_all_exported = Scene._get_all_export_dialog_files(skyrim_path)
        for ex in list_all_exported:
            if quest_id in ex:
                return ex
        return ""

    @staticmethod
    def _get_all_export_dialog_files(skyrim_path: str):
        """
        Return all the exported dialog files names inside Skyrim root directory.
        :param skyrim_path: The skyrim root directory.
        :return: list of expoted dialog files.
        """
        _log = Logger.get()
        _log.debug("_get_all_export_dialog_files()")
        all_files = [f for f in listdir(skyrim_path) if isfile(join(skyrim_path, f))]
        # filter all exported files from creation kit
        export_dialog_files = []
        for nth_file in all_files:
            if (nth_file.startswith(Consts.EXPORT_DIALOG_PREFIX) and
                    nth_file.endswith(Consts.EXPORT_DIALOG_EXT)):
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


if __name__ == '__main__':
    test_list_scene_quests = False
    test_export_scenes_to_csvdic = False
    test_build_scenes_list = False
    test_build_scenes_list2 = False
    text_export_scenes = True
    if test_list_scene_quests:
        ll = Scene.list_scene_quests("..\\Sandbox\\")
        for quest in ll:
            print("quest with scene: " + quest)
    if test_export_scenes_to_csvdic:
        [all_scene_files, quest_scenes_no_duplicates] = \
            Scene.export_scenes_to_csvdic("..\\Sandbox\\", "..\\SceneOrder.csv")
        print("all_scene_files: ")
        for sf in all_scene_files:
            print("    - " + sf)
        print("quest_scenes_no_duplicates:")
        for t in quest_scenes_no_duplicates:
            print("    - " + t[0] + ", " + t[1])
    if test_build_scenes_list:
        Scene.build_scenes_list("..\\Sandbox\\", "DSilHand_M80AssaultJor", "..\\SceneOrder.csv", "..\\Comments.csv", "..\\Actors.csv")
    if test_build_scenes_list2:
        # test the border cases
        Scene.build_scenes_list("..\\Sandbox\\", "M10SilverHunt", "..\\SceneOrder.csv")
    if text_export_scenes:
        Scene.export_scenes_to_csvdic("..\\Sandbox\\", "..\\SceneOrder.csv", "..\\Comments.csv", "..\\Actors.csv")

