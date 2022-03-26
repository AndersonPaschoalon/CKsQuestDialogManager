from PyUtils.FileUtils import *


class AudioData:
    """
    Stores audio data and information.
    """

    def __init__(self, file_path: str, quest_id: str, actor_name: str, subtitle: str, file_name="", dialog_type="",
                 emotion="", voice_type="", topic_id="", branch_id="", scene_id="", scene_phase=-1):
        """

        :param file_path: Full file name.
        :param quest_id: Quest ID.
        :param actor_name: Actor ID.
        :param subtitle: Subtitle text.
        :param file_name: Filename with
        :param dialog_type: Scene/Topic.
        :param emotion: Emotion data.
        :param voice_type: Voice Type data.
        :param topic_id: Topic ID.
        :param branch_id: Branch ID.
        :param scene_id: Scene ID.
        :param scene_phase: Scene Phase.
        """
        self.file_name = file_name
        self.actor_name = actor_name
        self.subtitle = subtitle
        self.quest_id = quest_id
        self.file_path = FileUtils.remove_ext(file_path)
        self.dialog_type = dialog_type
        self.emotion = emotion
        self.voice_type = voice_type
        self.topic_id = topic_id
        self.branch_id = branch_id
        self.scene_id = scene_id
        self.scene_phase = scene_phase

    def to_string(self):
        return "todo"

    def file_path_wav(self):
        return self.file_path + EXT_WAV

    def file_path_xwm(self):
        return self.file_path + EXT_XWM

    def file_path_fuz(self):
        return self.file_path + EXT_FUZ





