from PyUtils.Obj2Json import Obj2Json


class DialogLine:
    """
    A Dialog line represents each phrase said by each character in a Scene. A collection of ordered phases
    said by a single characters (DialogLine) forms a SceneTopic. A sequence of ordere SceneTopics represents a
    Scene.
    This object stores a Scene dialog line, combining information from the files dialogExport and SceneDialog_.
    To fill the properties, two methods should be used:  set_scene_dialog() and set_dialog_export().
    """

    def __init__(self):
        """
        Default constructor.
        """
        # SceneDialogue.FILENAME (key)
        self.sd_filename = ""
        # SceneDialogue.RESPONSE TEXT	SUPPORTING DIALOGUE
        self.sd_dialogue = ""
        # SceneDialogue.EMOTION
        self.sd_emotion = ""
        # SceneDialogue.SCRIPT NOTES
        self.sd_notes = ""
        # dialogueExport.RESPONSE INDEX
        self.de_response_index = ""
        # dialogExport.FULL PATH
        self.de_filepath = ""
        # flags to tell if the set methods where called
        self.flag_scene_dialog = False
        self.flag_dialog_export = False

    def set_scene_dialog(self, filename: str, dialogue: str, emotion: str, notes: str):
        """
        Set a Dialog Line data from a SceneDialog_ file.
        :param filename: 'FILENAME' column.
        :param dialogue: 'RESPONSE TEXT' or 'SUPPORTING DIALOGUE' column.
        :param emotion: 'EMOTION' column.
        :param notes: 'SCRIPT NOTES' column.
        :return: void
        """
        # SceneDialogue.FILENAME (key)
        self.sd_filename = filename
        # SceneDialogue.RESPONSE TEXT	SUPPORTING DIALOGUE
        self.sd_dialogue = dialogue
        # SceneDialogue.EMOTION
        self.sd_emotion = emotion
        # SceneDialogue.SCRIPT NOTES
        self.sd_notes = notes
        # set flag
        self.flag_scene_dialog = True

    def set_dialog_export(self, response_index: int, filepath: str):
        """
        Set a Dialog Line data from a dialogueExport file.
        :param response_index: 'RESPONSE INDEX' column.
        :param filepath: 'RESPONSE INDEX' column.
        :return: void.
        """
        # dialogueExport.RESPONSE INDEX
        self.de_response_index = response_index
        # dialogExport.RESPONSE INDEX
        self.de_filepath = filepath
        # set flag
        self.flag_dialog_export = True

    def to_string(self):
        obj = Obj2Json()
        obj.add("response_index", self.de_response_index)
        obj.add("filename", self.sd_filename)
        obj.add("filepath", self.de_filepath)
        obj.add("dialogue", self.sd_dialogue)
        obj.add("emotion", self.sd_emotion)
        obj.add("notes", self.sd_notes)
        obj.add("flag_dialog_export", self.flag_dialog_export)
        obj.add("flag_scene_dialog", self.flag_scene_dialog)
        return obj.json()

    def is_ready(self):
        """
        Tells if both set methods set_scene_dialog() and set_dialog_export(), where called, so the object is ready
        to be consumed.
        :return: True if the object is ready, False otherwise.
        """
        if self.flag_scene_dialog and self.flag_dialog_export:
            return True
        else:
            return False
