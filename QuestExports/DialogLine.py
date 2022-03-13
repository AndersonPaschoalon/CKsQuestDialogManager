from PyUtils.Obj2Json import Obj2Json

class DialogLine:
    """

    """
    def __init__(self):
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

    def set_scene_dialog(self, filename: str, dialogue: str, emotion: str, notes: str):
        # SceneDialogue.FILENAME (key)
        self.sd_filename = filename
        # SceneDialogue.RESPONSE TEXT	SUPPORTING DIALOGUE
        self.sd_dialogue = dialogue
        # SceneDialogue.EMOTION
        self.sd_emotion = emotion
        # SceneDialogue.SCRIPT NOTES
        self.sd_notes = notes

    def set_dialog_export(self, response_index: int, filepath: str):
        # dialogueExport.RESPONSE INDEX
        self.de_response_index = response_index
        # dialogExport.FULL PATH
        self.de_filepath = filepath

    def to_string(self):
        obj = Obj2Json()
        obj.add("response_index", self.de_response_index)
        obj.add("filename", self.sd_filename)
        obj.add("filepath", self.de_filepath)
        obj.add("dialogue", self.sd_dialogue)
        obj.add("emotion", self.sd_emotion)
        obj.add("notes", self.sd_notes)
        return obj.json()


