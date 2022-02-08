from .TopicDialogs import TopicDialogs
from PyUtils.Obj2Json import Obj2Json


class BranchDialogs:

    def __init__(self):
        """Default TopicDialogs constructor"""
        # branch name
        self.branch_name = ""
        # a description of the scene/dialog of the current branch
        self.description = ""
        # Actor name ID
        self.actor_name = ""
        # Eg.: MaleCommoner
        self.actor_voice_type = ""
        # Eg.: DarkElfRace, NordRace
        self.actor_race = ""
        # Type of dialog PlayerDialogue, SceneDialogue
        self.dialog_type = ""
        # tells of this object is ready to be used or not
        self.is_read = False
        # list of TopicDialogs in this branch
        self.list_topic_dialogs = []

    def to_string(self):
        obj = Obj2Json()
        obj.add("branch_name", self.branch_name)
        obj.add("description", self.description)
        obj.add("actor_name", self.actor_name)
        obj.add("actor_voice_type", self.actor_voice_type)
        obj.add("actor_race", self.actor_race)
        obj.add("actor_voice_type", self.actor_voice_type)
        obj.add("dialog_type", self.dialog_type)
        obj.add("is_read", self.is_read)
        topic_list_str = []
        for tp in self.list_topic_dialogs:
            topic_list_str.append(tp.to_string())
        obj.addl("list_topic_dialogs", topic_list_str)
        return obj.obj()

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
