from .TopicDialogs import TopicDialogs
from PyUtils.Obj2Json import Obj2Json


class BranchDialogs:

    def __init__(self):
        """Default TopicDialogs constructor"""
        # branch name
        self.branch_name = ""
        # a comment of the scene/dialog of the current branch
        self.comment = ""
        # Actor name ID
        self.actor_name = ""
        # Eg.: MaleCommoner
        self.actor_voice_type = ""
        # Eg.: DarkElfRace, NordRace
        self.actor_race = ""
        # Type of dialog PlayerDialogue, SceneDialogue
        self.dialog_type = ""
        # tells of this object is ready to be used or not
        self.is_ready = False
        # list of TopicDialogs in this branch
        self.list_topic_dialogs = []

    def is_branch_data_empty(self):
        """
        Tells if the topic data is empty of not.
        :return: True if it is empty, false otherwise.
        """
        # if there is not topics, it is empty
        if len(self.list_topic_dialogs) == 0:
            return True
        tp: TopicDialogs
        for tp in self.list_topic_dialogs:
            # if any is not empty, it is not empty
            if not tp.is_topic_data_empty():
                return False
        # all topics are empty
        return True

    def to_string(self):
        obj = Obj2Json()
        obj.add("branch_name", self.branch_name)
        obj.add("comment", self.comment)
        obj.add("actor_name", self.actor_name)
        obj.add("actor_voice_type", self.actor_voice_type)
        obj.add("actor_race", self.actor_race)
        obj.add("actor_voice_type", self.actor_voice_type)
        obj.add("dialog_type", self.dialog_type)
        obj.add("is_read", self.is_ready)
        topic_list_str = []
        for tp in self.list_topic_dialogs:
            topic_list_str.append(tp.to_string())
        obj.addl("list_topic_dialogs", topic_list_str)
        return obj.json()

    def add_topic_dialog(self, topic_dialog: TopicDialogs):
        """Adds TopicDialogs."""
        self.list_topic_dialogs.append(topic_dialog)

    def clear_topic_dialog(self):
        """Add topic dialog."""
        self.list_topic_dialogs.clear()

    def sort_name(self):
        """The topics dialogs by name"""
        self.list_topic_dialogs = sorted(self.list_topic_dialogs, key=lambda x: x.topic_name)

    def sort_formid(self):
        """The topics dialogs by Form ID"""
        self.list_topic_dialogs = sorted(self.list_topic_dialogs, key=lambda x: x.form_id)
