# lib imports
import csv
from os import listdir
from os.path import isfile, join
# local imports
from PyUtils.Console import Console
from PyUtils.Cd import Cd
from PyUtils.Logger import Logger
from PyUtils.Obj2Json import Obj2Json
from PyUtils.Functions import *

from .TopicDialogs import TopicDialogs
from .BranchDialogs import BranchDialogs


class QuestDialogs:
    """
    This class stores information about the quest dialogs, parsers the Creation Kit exported files,
    and generates the documentation.
    """
    # file
    LABEL_FILE_FULL_PATH = 'FULL PATH'
    EXPORT_DIALOG_PREFIX = "dialogueExport"
    EXPORT_DIALOG_EXT = ".txt"
    # quest
    LABEL_QUEST_QUEST = 'QUEST'
    LABEL_QUEST_BRANCH = 'BRANCH'
    LABEL_QUEST_TOPIC = 'TOPIC'
    LABEL_QUEST_TYPE = 'TYPE'
    LABEL_QUEST_FORM_ID = 'TOPICINFO'
    # player
    LABEL_PLAYER_PROMPT = 'PROMPT'  # player dialog text
    # npc 1xbranch
    LABEL_NPC_SPEAKER = 'SPEAKER'
    LABEL_NPC_RACE = 'RACE'
    LABEL_NPC_VOICE_TYPE = 'VOICE TYPE'
    # NPC nxbranch
    LABEL_NPC_RESPONSE_INDEX = 'RESPONSE INDEX'
    LABEL_NPC_RESPONSE_TEXT = 'RESPONSE TEXT'  # npc dialog text
    LABEL_NPC_EMOTION = 'EMOTION'
    # default values
    DEFAULT_BRANCH_DESCRIPTION = "?banch-comment?"
    DEFAULT_QUEST_DESCRIPTION = "?banch-comment?"

    def __init__(self, quest_name: str, quest_description: str):
        """ Quest dialog default constructor"""
        self._quest_name = quest_name
        self._comment = text(quest_description)
        self._list_branch_dialogs = []

    def to_string(self):
        obj = Obj2Json()
        obj.add("_quest_name", self._quest_name)
        obj.add("_comment", self._comment)
        list_branch_str = []
        for br in self._list_branch_dialogs:
            list_branch_str.append(br.to_string())
        obj.addl("_list_branch_dialogs", list_branch_str)
        return obj.json()


    def add_branch_dialog(self, branch_dialog: BranchDialogs):
        """ """
        self._list_branch_dialogs.append(branch_dialog)

    def clear_branch_dialog(self):
        """"""
        self._list_branch_dialogs.clear()

    def generate_markdown(self, destination):
        """"""
        print("todo")

    @staticmethod
    def build_quest_objects(skyrim_path):
        """"""
        log = Logger.get_logger()
        all_files = [f for f in listdir(skyrim_path) if isfile(join(skyrim_path, f))]
        print(all_files)
        # filter all exported files from creation kit
        export_dialog_files = []
        for nth_file in all_files:
            if (nth_file.startswith(QuestDialogs.EXPORT_DIALOG_PREFIX) and
                    nth_file.endswith(QuestDialogs.EXPORT_DIALOG_EXT)):
                export_dialog_files.append(nth_file)
        # return if no file was filtered
        if len(export_dialog_files) == 0:
            Console.yellow("No valid Creation Kit exported file was found at directory <" + skyrim_path + ">")
            Console.yellow("** Check settings.ini, and try again.")
            return True

        # loop over all filtered files
        list_quest = []
        list_branches = []
        with Cd(skyrim_path):
            for nth_file in export_dialog_files:
                # erase the branches from the last file
                list_branches.clear()
                with open(nth_file) as fd:
                    rd = csv.reader(fd, delimiter="\t", quotechar='"')
                    # calc the positions for each file
                    first_row = next(rd)
                    col_file = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_FILE_FULL_PATH)
                    col_quest = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_QUEST_QUEST)
                    col_branch = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_QUEST_BRANCH)
                    col_topic = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_QUEST_TOPIC)
                    col_type = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_QUEST_TYPE)
                    col_form_id = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_QUEST_FORM_ID)
                    col_prompt = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_PLAYER_PROMPT)
                    col_npc = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_NPC_SPEAKER)
                    col_npc_race = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_NPC_RACE)
                    col_npc_voice = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_NPC_VOICE_TYPE)
                    col_npc_resp_index = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_NPC_RESPONSE_INDEX)
                    col_npc_resp_text = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_NPC_RESPONSE_TEXT)
                    col_npc_resp_emo = QuestDialogs.get_index(first_row, QuestDialogs.LABEL_NPC_EMOTION)

                    quest_name = ""
                    last_branch = ""
                    current_branch = ""
                    last_topic = ""
                    current_topic = ""
                    branch_obj = BranchDialogs()
                    topic_obj = TopicDialogs()
                    list_topics = []
                    for row in rd:

                        # store the quest name
                        if quest_name == "":
                            quest_name = row[col_quest]

                        # create a new branch of necessary
                        current_branch = row[col_branch]
                        if last_branch == "" or last_branch != current_branch:
                            # Stores data from the last iteration
                            # * If it is a new branch, the last topic needs to be stored now -- if the branch is ready
                            #   (not the first)
                            QuestDialogs.add_topic(branch_obj, last_topic, topic_obj)
                            # stores the last branch on the list if it is a new one and not the first
                            QuestDialogs.add_branch(list_branches, last_branch, branch_obj)
                            # update last_branch string
                            last_branch = current_branch
                            # a new branch started, fills the object branch data
                            branch_obj = BranchDialogs()
                            branch_obj.branch_name = current_branch
                            branch_obj.comment = QuestDialogs.DEFAULT_BRANCH_DESCRIPTION
                            branch_obj.dialog_type = row[col_type]
                            branch_obj.actor_name = row[col_npc]
                            branch_obj.actor_race = row[col_npc_race]
                            branch_obj.actor_voice_type = row[col_npc_voice]
                            branch_obj.is_read = True

                        # updates the topic of this new line
                        current_topic = row[col_topic]
                        # check if a new topic need to be created
                        if last_topic == "" or last_topic != current_topic:
                            # add the last topic object to the branch object
                            QuestDialogs.add_topic(branch_obj, last_topic, topic_obj)
                            # a new topic started, a new one needs to be created
                            topic_obj = TopicDialogs()
                            topic_obj.topic_name = row[col_topic]
                            topic_obj.actor_name = row[col_npc]
                            topic_obj.player_dialog = row[col_prompt]
                            topic_obj.form_id = row[col_form_id]
                            # update last topic
                            last_topic = current_topic
                        # endif
                        # add current line data to the topic object -- one per line
                        str_index = row[col_npc_resp_index]
                        str_dialogue = text(row[col_npc_resp_text])
                        str_mood = row[col_npc_resp_emo]
                        topic_obj.add_topic_data(str_index, str_dialogue, str_mood)
                    # endfor
                # endwith
                # Stores the data from the last iteration
                # add last topic
                QuestDialogs.add_topic(branch_obj, last_topic, topic_obj)
                # add last branch
                QuestDialogs.add_branch(list_branches, last_branch, branch_obj)
                # now, we can create the new quest object :D
                quest = QuestDialogs(quest_name, QuestDialogs.DEFAULT_QUEST_DESCRIPTION)
                for br in list_branches:
                    quest.add_branch_dialog(br)
                # endfor
                list_quest.append(quest)
                Console.green("* File " + nth_file + " processed!")
            # endfor
        Console.green("Number of files processed: " + str(len(list_quest)))
        for q in list_quest:
            print(q.to_string())

    @staticmethod
    def get_index(first_row, label):
        print(first_row)
        if len(first_row) == 0:
            return 0
        return first_row.index(label)

    @staticmethod
    def add_branch(list_branches: list, last_branch: str, branch_object: BranchDialogs):
        """
        This method should be used when recovering a new exported line, of after the end of the last line (to process
        the last line of the file)
        If the last branch name is empty, that means if is the first row of the matrix, so no branch as created
        yet. Therefore there is no need to add data to the list.
        If the last_branch is a not empty string, that means it is a new branch, and must be added.
        It must be used only after the developer check if the branch really need to be added.
        """
        if last_branch == "":
            return
        branch_object.sort_name()
        list_branches.append(branch_object)

    @staticmethod
    def add_topic(branch_object: BranchDialogs, last_topic: str, topic: TopicDialogs):
        """
        This method should be used when recovering a new exported line, of after the end of the last line (to process
        the last line of the file)
        If the last topic name is empty, that means if is the first row of the matrix, so no topic as created
        yet. Therefore there is no need to add data to the BranchDialogs object.
        If the last_branch is a not empty string, that means it is a new branch, and must be added.
        It must be used only after the developer check if the branch really need to be added.
        """
        # if it is the first processed line, and no branch is ready
        if not branch_object.is_read:
            return
        if last_topic == "":
            return
        # topic.sort()
        branch_object.add_topic_dialog(topic)

    @staticmethod
    def append_topic_dialog(branch: BranchDialogs, topic: TopicDialogs):
        if branch.is_read:
            branch.add_topic_dialog(topic)


if __name__ == '__main__':
    QuestDialogs.build_quest_objects("../Sandbox/")