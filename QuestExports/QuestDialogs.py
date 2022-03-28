from os import listdir
from os.path import isfile, join
import markdown
from htmldocx import HtmlToDocx
from PyUtils.Console import Console
from PyUtils.Cd import Cd
from PyUtils.Logger import Logger
from PyUtils.Obj2Json import Obj2Json
from PyUtils.Functions import *
from PyUtils.CsvDic import *
from QuestExports.TopicDialogs import TopicDialogs
from QuestExports.BranchDialogs import BranchDialogs
from QuestExports.Consts import Consts
from QuestExports.Scene import Scene
from QuestExports.SceneTopic import SceneTopic
from QuestExports.DialogLine import DialogLine

"""
TODO: quando se criar os objectos da quest, as cenas devem ser adicionadas
TODO: no generate documentation, a cenas devem ser acessadas da quest.

"""

class QuestDialogs:
    """
    This class stores information about the quest dialogs, parsers the Creation Kit exported files,
    and generates the documentation.
    """
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
    DEFAULT_QUEST_DESCRIPTION = "?quest-comment?"
    # CSV dics
    CSV_COMMENTS_DELIMITER = ","
    CSV_ACTOR_DELIMITER = ","
    CSV_EMPTY_COLUMN = "--"
    """
    _log = None

    def __init__(self, quest_name: str, quest_description: str, skyrim_path: str):
        """
        Contructor for the QuestDialogs object. Should to be used, you must call the static method
        build_quest_objects() instead.
        :param quest_name: The quest ID name.
        :param quest_description: A quest description.
        """
        self.quest_name = quest_name
        self.comment = text(quest_description)
        self.skyrim_path = skyrim_path
        self.list_branch_dialogs = []
        self.list_scenes = []
        self._log = Logger.get()

    def to_string(self):
        """
        Retruns a string representation of the QuestDialog object on Json format.
        :return:
        """
        obj = Obj2Json()
        obj.add("quest_name", self.quest_name)
        obj.add("comment", self.comment)
        obj.add("skyrim_path", self.skyrim_path)
        list_branch_str = []
        for br in self.list_branch_dialogs:
            list_branch_str.append(br.to_string())
        obj.addl("list_branch_dialogs", list_branch_str)
        list_scenes_str = []
        for sc in self.list_scenes:
            list_scenes_str.append(sc.to_string())
        obj.addl("list_scenes", list_scenes_str)
        return obj.json()

    def generate_documentation(self, destination):
        """
        This method generate the actual documentation.
        :param destination: The directory where the documentation will be generated.
        :return: void
        """
        # (1) Initialize environment
        self._log.debug("generate_documentation() destination:" + destination + " for quest " + self.quest_name)
        doc_html = destination + Consts.DOC_HTML_DIR
        doc_md = destination + Consts.DOC_MD_DIR
        doc_json = destination + Consts.DOC_JSON_DIR
        doc_docx = destination + Consts.DOC_DOCX_DIR
        if not os.path.exists(destination):
            os.makedirs(destination)
        if not os.path.exists(doc_html):
            os.makedirs(doc_html)
        if not os.path.exists(doc_md):
            os.makedirs(doc_md)
        if not os.path.exists(doc_json):
            os.makedirs(doc_json)
        if not os.path.exists(doc_docx):
            os.makedirs(doc_docx)
        path_html = doc_html + self.quest_name + Consts.DOC_HTML_EXT
        path_md = doc_md + self.quest_name + Consts.DOC_MD_EXT
        path_json = doc_json + self.quest_name + Consts.DOC_JSON_EXT
        path_docx = doc_docx + self.quest_name
        md = ""
        md += "# Quest {0}\n".format(self.quest_name)
        md += "\n_{0}_\n".format(self.comment.strip().replace('_', '\\_'))
        branch: BranchDialogs
        topic: TopicDialogs
        # (2) Creating quest branches documentation
        md += "\n## Branches\n"
        for branch in self.list_branch_dialogs:
            if not branch.is_branch_data_empty():
                md += "### {0}\n".format(branch.branch_name)
                md += "> _{0}_\n".format(branch.comment.strip())
                md += "> \n"
                md += "> Dialog Type:``{0}``, Actor Race:``{1}``, Voice Type:``{2}``.\n\n".format(branch.dialog_type.strip(),
                                                                                                  branch.actor_race.strip(),
                                                                                                  branch.actor_voice_type.strip())
                for topic in branch.list_topic_dialogs:

                    self._log.debug("=> TOPIC :" + topic.topic_name + ":" + str(len(topic._list_topic_data)))
                    if not topic.is_topic_data_empty():
                        md += "#### {0}\n\n".format(topic.topic_name)
                        if topic.comment.strip() != "":
                            md += "{0}\n\n".format(topic.comment.strip().replace('_', '\\_'))
                        md += "{0}: {1}\n\n".format(Consts.STR_PLAYER_VAL, topic.player_dialog)
                        for npc_data in topic.get_topic_data():
                            md += "{0} ({1}): {2}    \n\n".format(topic.actor_name, npc_data[2], npc_data[1])
                            md += "``{0}``    \n\n".format(npc_data[3])
                        md += "\n"
                    else:
                        self._log.warning("** TOPIC DATA IS EMPTY FOR TOPIC <" + topic.topic_name + "> **")
                        self._log.warning("** TOPIC <" + topic.topic_name +
                                          "> IS NOT GOING TO BE ADDED TO THE DOCUMENTATION  **")
            else:
                self._log.warning("** BRANCH DATA IS EMPTY FOR BRANCH <" + branch.branch_name + "> **")
                self._log.warning("** BRANCH <" + branch.branch_name +
                                  "> IS NOT GOING TO BE ADDED TO THE DOCUMENTATION  **")
        # (3) Creating quest scenes documentation
        is_empty = True
        # Check if list is empty
        scene: Scene
        for scene in self.list_scenes:
            if not scene.is_empty():
                is_empty = False
        if not is_empty:
            # Create scene documentation for scene
            md += "\n## Scenes\n"
            for scene in self.list_scenes:
                if not scene.is_empty():
                    md += "### {0}\n".format(scene.scene_id)
                    if scene.comment.strip() != "":
                        md += "{0}\n\n".format(scene.comment.strip().replace('_', '\\_'))
                    st: SceneTopic
                    for st in scene.list_scene_topics:
                        md += "#### Phase {0}: {1}\n\n".format(st.scene_phase(), st.actor_name())
                        md +="> Dialog Type:``{0}``, Actor Race:``{1}``, Voice Type:``{2}``.\n\n".\
                            format(st.dialog_type(), st.actor_race(), st.voice_type())
                        dl: DialogLine
                        for dl in st.sd_list_dialog_lines:
                            md += "({0}): {1}    \n\n".format(dl.emotion(), dl.dialogue())
                            md += "``{0}``    \n\n".format(dl.filepath())
                            if dl.notes() != "":
                                md += "Notes: *{0}*    \n\n".format(dl.notes())
                        md += "\n"
                else:
                    self._log.warn("**WARN** SKIPPING EMPTY SCENE.")
        else:
            self._log.info("!! THERE IS NO SCENE FOR QUEST <" + self.quest_name + "> !!")
        # (3) Creating documentation footer
        md += "\n\n\n*****\n\n"
        md += "> _Documentation generated by {0}. Access the project <a href=\"{1}\" target=\"_blank\">Github</a> for new versions and updates._\n\n"\
            .format(Consts.APP_NAME, Consts.URL_GITHUB)
        self._log.debug("markdown generated -> saving into files")
        # (4) Generating documentation
        # Markdown
        self._log.debug("creating markdown")
        md_file = open(path_md, "w")
        md_file.write(md)
        md_file.close()
        # html
        self._log.debug("creating html")
        html_file = open(path_html, "w")
        html = markdown.markdown(md)
        html_file.write(html)
        html_file.close()
        # docx
        self._log.debug("creating docx")
        new_parser = HtmlToDocx()
        new_parser.parse_html_file(path_html, path_docx)
        # json
        self._log.debug("creating json")
        jfile = open(path_json, "w")
        jfile.write(self.to_string())
        jfile.close()

    def _add_branch_dialog(self, branch_dialog: BranchDialogs):
        """
        Add a new BranchDialog object to the list ob BranchDialogs of the quest.
        :param branch_dialog: add branch dialog list.
        :return: void
        """
        self.list_branch_dialogs.append(branch_dialog)

    def _add_scene(self, scene: Scene):
        """
        Add a new Scene object to the list ob BranchDialogs of the quest.
        :param scene: add branch dialog list.
        :return: void
        """
        self.list_scenes.append(scene)

    def _clear_branch_dialog(self):
        """
        Clean the list of branch dialogs from the quest object.
        :return: void
        """
        self.list_branch_dialogs.clear()

    @staticmethod
    def export_objects_to_csvdics(skyrim_path: str, comments_csv: str, actors_csv: str):
        """
        Export the object names into the CSV dictionaries: Comments.csv and Actors.csv.
        :param skyrim_path: Skyrim directory.
        :param comments_csv: Comment dictionary Comments.csv.
        :param actors_csv: Actors Names dictionary Actors.csv.
        :return: [exported_files, list_objects, list_actors]: returns 3 arrays, a list of exported files, a list of
        objects exported, and a list of actors exported.
        """
        _log = Logger.get()
        # load objects
        exported_files = QuestDialogs._get_all_export_dialog_files(skyrim_path)
        actors = CsvDic(actors_csv, Consts.CSV_ACTOR_DELIMITER)
        comments = CsvDic(comments_csv, Consts.CSV_COMMENTS_DELIMITER)
        # filter all objects and actors
        with Cd(skyrim_path):
            list_objects = []
            list_actors = []
            for nth_file in exported_files:
                with open(nth_file) as fd:
                    rd = csv.reader(fd, delimiter="\t", quotechar='"')
                    # calc the positions for each file
                    first_row = next(rd)
                    col_quest = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_QUEST_QUEST)
                    col_branch = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_QUEST_BRANCH)
                    col_npc = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_NPC_SPEAKER)
                    col_topic = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_QUEST_TOPIC)
                    for row in rd:
                        current_quest = row[col_quest]
                        current_branch = row[col_branch]
                        current_topic = row[col_topic]
                        current_npc = row[col_npc]
                        # add objects
                        if (current_quest is not None) and (current_quest != "") and \
                                (current_quest != Consts.CSV_EMPTY_COLUMN):
                            list_objects.append(current_quest)
                        if (current_branch is not None) and (current_branch != "") and \
                                (current_branch != Consts.CSV_EMPTY_COLUMN):
                            list_objects.append(current_branch)
                        if (current_topic is not None) and (current_topic != "") and \
                                (current_topic != Consts.CSV_EMPTY_COLUMN):
                            list_objects.append(current_topic)
                        # add actors
                        if (current_npc is not None) and (current_npc != "") and \
                                (current_npc != Consts.CSV_EMPTY_COLUMN):
                            list_actors.append(current_npc)
                        _log.debug("* objs: " + current_quest + ", " + current_branch + "" + current_topic)
        # go back to the working directory and remove duplicates
        list_objects = list(dict.fromkeys(list_objects))
        list_actors = list(dict.fromkeys(list_actors))
        _log.debug(list_actors)
        _log.debug(list_objects)
        for obj in list_objects:
            comments.add(obj, "")
        for act in list_actors:
            actors.add(act, "")
        _log.info("Exportation process completed.")
        return [exported_files, list_objects, list_actors]

    @staticmethod
    def generate_quest_documentation(skyrim_path: str, comment_csv: str, actors_csv: str, scene_order_csv: str, doc_dir: str):
        """
        Main method to generate the quest documentation.
        :param skyrim_path: place where the exported files from Creation Kit are going to be searched.
        :param comment_csv: Commensts.csv dictionary file.
        :param actors_csv: Actors.csv dictionary file.
        :param scene_order_csv: SceneOrder.csv dictionary file.
        :param doc_dir: Documentation output directory.
        :return: list of quests names for which the documentation was generated.
        """
        _log = Logger.get()
        _log.debug("generate_quest_documentation() skyrim_path:" + skyrim_path + ", comment_csv:" +
                   comment_csv + ", actors_csv:" + actors_csv + ", doc_dir:" + doc_dir)
        list_quests_names = []
        list_quest_obj = QuestDialogs.build_quest_objects(skyrim_path, comment_csv, actors_csv, scene_order_csv)
        for q in list_quest_obj:
            q.generate_documentation(doc_dir)
            list_quests_names.append(q.quest_name)
        print("Documentation generation finished.")
        _log.info("Documentation generation finished.")
        return list_quests_names

    @staticmethod
    def build_quest_objects(skyrim_path, comments_csv: str, actors_csv: str, scene_order_csv: str) -> list:
        """
        Build a list of QuestDialog objects using the exported files from creation kit in the directory
        skyrim_path, using as optional files he Comments.csv and Actors.csv dictionaries.
        :param skyrim_path: Skyrim instalation path, where the exported files from Creation Kit will be searched.
        :param comments_csv: The Comments.csv dictionary optional file.
        :param actors_csv: The Actors.csv dictionary optional file.
        :param scene_order_csv:  The SceneOrder.csv dictionary.
        :return: The list of QuestDialog objects.
        """
        _log = Logger.get()
        _log.debug("build_quest_objects(): skyrim_path:" + skyrim_path + ", comments_csv:" + comments_csv +
                   ", actors_csv:" + actors_csv + ", scene_order_csv:" + scene_order_csv)
        #
        # CREATE QUEST BRANCHES
        #
        # initialize output list
        list_quest = []
        comments = CsvDic(comments_csv, Consts.CSV_COMMENTS_DELIMITER)
        actors_dic = CsvDic(actors_csv, Consts.CSV_ACTOR_DELIMITER)
        export_dialog_files = QuestDialogs._get_all_export_dialog_files(skyrim_path)
        for ex_files in export_dialog_files:
            _log.debug(" exported file:" + ex_files)
        if len(export_dialog_files) == 0:
            # return if no file was filtered
            _log.warning("No valid Creation Kit exported file was found at directory <" + skyrim_path + ">")
            _log.warning("** Check settings.ini, and try again.")
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
                    col_file = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_FULL_PATH)
                    col_file_name = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_FILENAME)
                    col_quest = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_QUEST_QUEST)
                    col_branch = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_QUEST_BRANCH)
                    col_topic = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_QUEST_TOPIC)
                    col_type = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_QUEST_TYPE)
                    col_form_id = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_QUEST_FORM_ID)
                    col_prompt = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_PLAYER_PROMPT)
                    col_npc = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_NPC_SPEAKER)
                    col_npc_race = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_NPC_RACE)
                    col_npc_voice = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_NPC_VOICE_TYPE)
                    col_npc_resp_index = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_NPC_RESPONSE_INDEX)
                    col_npc_resp_text = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_NPC_RESPONSE_TEXT)
                    col_npc_resp_emo = QuestDialogs._get_index(first_row, Consts.LABEL_DIALOG_NPC_EMOTION)
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
                            _log.debug(" # ADD TOPIC " + topic_obj.topic_name + " TO BRANCH " + branch_obj.branch_name)
                            QuestDialogs._add_topic(branch_obj, last_topic, topic_obj)
                            is_topic_added = True
                            # stores the last branch on the list if it is a new one and not the first
                            QuestDialogs._add_branch(list_branches, last_branch, branch_obj)
                            # update last_branch string
                            last_branch = current_branch
                            # a new branch started, fills the object branch data
                            branch_obj = BranchDialogs()
                            branch_obj.branch_name = current_branch
                            branch_obj.comment = comments.get(current_branch, Consts.DEFAULT_BRANCH_DESCRIPTION)
                            # delete
                            _log.debug("-- comments._csv_file:" + comments._csv_file)
                            branch_obj.dialog_type = row[col_type]
                            # branch_obj.actor_name = row[col_npc]
                            actor_id = row[col_npc]
                            branch_obj.actor_name = actors_dic.get(actor_id, actor_id)
                            branch_obj.actor_race = row[col_npc_race]
                            branch_obj.actor_voice_type = row[col_npc_voice]
                            branch_obj.is_ready = True
                        # updates the topic of this new line
                        current_topic = row[col_topic]
                        # check if a new topic need to be created
                        if last_topic == "" or last_topic != current_topic:
                            # add the last topic object to the branch object
                            _log.debug(" * ADD TOPIC " + topic_obj.topic_name + " TO BRANCH " + branch_obj.branch_name)
                            if not is_topic_added:
                                QuestDialogs._add_topic(branch_obj, last_topic, topic_obj)
                            # a new topic started, a new one needs to be created
                            topic_obj = TopicDialogs()
                            topic_obj.topic_name = row[col_topic]
                            # topic_obj.actor_name = row[col_npc]
                            actor_id = row[col_npc]
                            topic_obj.actor_name = actors_dic.get(actor_id, actor_id)
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
                        str_file = row[col_file]
                        str_file_name = row[col_file_name]
                        topic_obj.add_topic_data(str_index, str_dialogue, str_mood, str_file, str_file_name)
                    # endfor
                # endwith
                # Stores the data from the last iteration
                # add last topic
                QuestDialogs._add_topic(branch_obj, last_topic, topic_obj)
                # add last branch
                QuestDialogs._add_branch(list_branches, last_branch, branch_obj)
                # now, we can create the new quest object :D
                quest_comment = comments.get(quest_name, Consts.DEFAULT_QUEST_DESCRIPTION)
                _log.info("-- quest_name:" + quest_name + ", quest_comment:" + quest_comment)
                quest = QuestDialogs(quest_name, quest_comment, skyrim_path)
                for br in list_branches:
                    quest._add_branch_dialog(br)
                # endfor
                list_quest.append(quest)
                Console.green("* File " + nth_file + " processed!")
                _log.info("* File " + nth_file + " processed!")
            # endfor
        _log.info("Number of files processed: " + str(len(list_quest)))
        #
        # CREATE SCENES
        #
        scenes_quests = Scene.list_scene_quests(skyrim_path)
        i = 0
        while i < len(list_quest):
            curr_quest_name = list_quest[i].quest_name
            if curr_quest_name in scenes_quests:
                scene_list = Scene.build_scenes_list(skyrim_path, curr_quest_name,
                                                     scene_order_csv, comments_csv, actors_csv)
                _log.debug("amount of scenes for quest " + curr_quest_name + ": " + str(len(scene_list)))
                for scene in scene_list:
                    _log.debug("adding scene " + scene.scene_id + " to quest " + curr_quest_name)
                    list_quest[i]._add_scene(scene)
            i += 1
        # debug information
        counter_quest = 0
        for q in list_quest:
            _log.debug("-- Quest Object [" + str(counter_quest) + "]: " + q.to_string())
            counter_quest += 1
        return list_quest

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
    def _add_branch(list_branches: list, last_branch: str, branch_object: BranchDialogs):
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
    def _add_topic(branch_object: BranchDialogs, last_topic: str, topic: TopicDialogs):
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
        branch_object.add_topic_dialog(topic)

    @staticmethod
    def _append_topic_dialog(branch: BranchDialogs, topic: TopicDialogs):
        """
        Append a new dialog object to a branch object, if it is already initialized.
        :param branch: The main branch object.
        :param topic: The new topic to be added.
        :return:
        """
        if branch.is_ready:
            branch.add_topic_dialog(topic)

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
            if (nth_file.startswith(Consts.EXPORT_DIALOG_PREFIX) and
                    nth_file.endswith(Consts.EXPORT_DIALOG_EXT)):
                export_dialog_files.append(nth_file)
        return export_dialog_files


if __name__ == '__main__':
    QuestDialogs.build_quest_objects("..\\Sandbox", "..\\Comments.csv", "..\\Actors.csv", "..\\SceneOrder.csv")
