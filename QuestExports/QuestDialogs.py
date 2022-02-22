# lib imports
import csv
from os import listdir
from os.path import isfile, join
import markdown
from docx import Document
from htmldocx import HtmlToDocx
# local imports
from PyUtils.Console import Console
from PyUtils.Cd import Cd
from PyUtils.Logger import Logger
from PyUtils.Obj2Json import Obj2Json
from PyUtils.Functions import *
from PyUtils.CsvDic import *

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
    # CSV dics
    CSV_COMMENTS_DELIMITER = ";"
    CSV_ACTOR_DELIMITER = ";"

    def __init__(self, quest_name: str, quest_description: str, comment_file="../Comments.csv"):
        """ Quest dialog default constructor"""
        self.quest_name = quest_name
        self.comment = text(quest_description)
        self.comment_file = comment_file
        self.list_branch_dialogs = []

    def to_string(self):
        obj = Obj2Json()
        obj.add("quest_name", self.quest_name)
        obj.add("comment", self.comment)
        list_branch_str = []
        for br in self.list_branch_dialogs:
            list_branch_str.append(br.to_string())
        obj.addl("list_branch_dialogs", list_branch_str)
        return obj.json()

    def add_branch_dialog(self, branch_dialog: BranchDialogs):
        """ """
        self.list_branch_dialogs.append(branch_dialog)

    def clear_branch_dialog(self):
        """"""
        self.list_branch_dialogs.clear()

    def generate_documentation(self, destination="./Docs/Md/"):
        """"""
        STR_PLAYER = "Player"
        md = ""
        md += "# Quest {0}\n\n".format(self.quest_name)
        branch: BranchDialogs
        topic: TopicDialogs
        for branch in self.list_branch_dialogs:
            md += "## {0}\n\n".format(branch.branch_name)
            md += "> _{0}_\n\n".format(branch.comment)
            for topic in branch.list_topic_dialogs:
                md += "* {0}\n\n".format(topic.topic_name)
                md += "    {0}: {1}\n\n".format(STR_PLAYER, topic.player_dialog)
                for npc_data in topic.get_topic_data():
                    md += "    {0}({1}): {2}\n\n".format(topic.actor_name, npc_data[2], npc_data[1])
        # Markdown
        md_file = open(self.quest_name + ".md", "w")
        md_file.write(md)
        md_file.close()
        # html
        md_file = open(self.quest_name + ".html", "w")
        html = markdown.markdown(md)
        md_file.write(html)
        md_file.close()
        # docx
        new_parser = HtmlToDocx()
        new_parser.parse_html_file(self.quest_name + ".html", self.quest_name + ".docx")

    @staticmethod
    def export_ids_to_actors_file(skyrim_path: str, comment_csv: str):
        print("todo")


    @staticmethod
    def export_objects_to_comment_file(skyrim_path: str, comment_csv: str):
        print("todo")


    @staticmethod
    def generate_quest_documentation(skyrim_path: str, comment_csv: str, doc_dir: str):
        list_quest_obj = QuestDialogs.build_quest_objects(skyrim_path, comment_csv)
        for q in list_quest_obj:
            with open(q.quest_name + ".json", "w") as text_file:
                text_file.write(q.to_string())
            q.generate_documentation(doc_dir)
        print("Documentation generation finished.")

    @staticmethod
    def build_quest_objects(skyrim_path, comments_csv: str, actors_csv: str) -> list:
        """
        Build a list of QuestDialog objects using the exported files from creation kit in the directory
        skyrim_path, using as optional files he Comments.csv and Actors.csv dictionaries.
        :param skyrim_path: Skyrim instalation path, where the exported files from Creation Kit will be searched.
        :param comments_csv: The Comments.csv dictionary optional file.
        :param actors_csv: The Actors.csv dictionary optional file.
        :return: The list of QuestDialog objects.
        """
        # initialize output list
        list_quest = []
        comments = CsvDic(comments_csv)
        log = Logger.get_logger()
        all_files = [f for f in listdir(skyrim_path) if isfile(join(skyrim_path, f))]
        # print(all_files)
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
            return list_quest

        # loop over all filtered files
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

                    # clear variables
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
                        # tells if the topic was already added
                        is_topic_added = False
                        # create a new branch if necessary
                        current_branch = row[col_branch]
                        if last_branch == "" or last_branch != current_branch:
                            # Stores data from the last iteration
                            # * If it is a new branch, the last topic needs to be stored now -- if the branch is ready
                            #   (not the first)
                            # print(" # ADD TOPIC " + topic_obj.topic_name + " TO BRANCH " + branch_obj.branch_name)
                            QuestDialogs.add_topic(branch_obj, last_topic, topic_obj)
                            is_topic_added = True
                            # stores the last branch on the list if it is a new one and not the first
                            QuestDialogs.add_branch(list_branches, last_branch, branch_obj)
                            # update last_branch string
                            last_branch = current_branch
                            # a new branch started, fills the object branch data
                            branch_obj = BranchDialogs()
                            branch_obj.branch_name = current_branch
                            branch_obj.comment = comments.get(current_branch, QuestDialogs.DEFAULT_BRANCH_DESCRIPTION)
                            branch_obj.dialog_type = row[col_type]
                            branch_obj.actor_name = row[col_npc]
                            branch_obj.actor_race = row[col_npc_race]
                            branch_obj.actor_voice_type = row[col_npc_voice]
                            branch_obj.is_ready = True

                        # updates the topic of this new line
                        current_topic = row[col_topic]
                        # check if a new topic need to be created
                        if last_topic == "" or last_topic != current_topic:
                            # add the last topic object to the branch object
                            # print(" * ADD TOPIC " + topic_obj.topic_name + " TO BRANCH " + branch_obj.branch_name)
                            if not is_topic_added:
                                QuestDialogs.add_topic(branch_obj, last_topic, topic_obj)
                            # a new topic started, a new one needs to be created
                            topic_obj = TopicDialogs()
                            topic_obj.topic_name = row[col_topic]
                            topic_obj.actor_name = row[col_npc]
                            topic_obj.player_dialog = row[col_prompt]
                            topic_obj.form_id = row[col_form_id]
                            topic_obj.comment = comments.get(current_topic, "")
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
                quest_comment = comments.get(quest_name, QuestDialogs.DEFAULT_QUEST_DESCRIPTION)
                quest = QuestDialogs(quest_name, quest_comment)
                for br in list_branches:
                    quest.add_branch_dialog(br)
                # endfor
                list_quest.append(quest)
                Console.green("* File " + nth_file + " processed!")
            # endfor
        Console.green("Number of files processed: " + str(len(list_quest)))
        #for q in list_quest:
        #    text_file = open(q.quest_name + ".json", "w")
        #    text_file.write(q.to_string())
        #    text_file.close()
        #    q.generate_documentation()
        return list_quest

    @staticmethod
    def get_index(first_row, label):
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
    def add_branch(list_branches: list, last_branch: str, branch_object: BranchDialogs):
        """
        Private Method.
        This method should be used when recovering a new exported line to be proceced, or after the end of the
        last line (to process the last line of the file) of the exported dialogues file from Creation Kit.
        If the last branch name is empty, that means if is the first row of the matrix, so no branch as created
        yet. Therefore there is no need to add data to the list.
        If the last_branch is a not empty string, that means it is a new branch, and must be added.
        It must be used only after the developer check if the branch really need to be added.
        :param list_branches:
        :param last_branch:
        :param branch_object:
        :return:
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
        :param branch_object:
        :param last_topic:
        :param topic:
        :return:
        """
        # if it is the first processed line, and no branch is ready
        if not branch_object.is_ready:
            return
        if last_topic == "":
            return
        # topic.sort()
        branch_object.add_topic_dialog(topic)

    @staticmethod
    def append_topic_dialog(branch: BranchDialogs, topic: TopicDialogs):
        """
        Append a new dialog object to a branch object, if it is already initialized.
        :param branch: The main branch object.
        :param topic: The new topic to be added.
        :return:
        """
        if branch.is_ready:
            branch.add_topic_dialog(topic)


if __name__ == '__main__':
    QuestDialogs.build_quest_objects("../Sandbox/")