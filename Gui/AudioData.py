from PyUtils.FileUtils import Exts
from PyUtils.FileUtils import FileUtils
from PyUtils.Obj2Json import Obj2Json
from QuestExports.QuestDialogs import QuestDialogs
from QuestExports.Scene import Scene
from QuestExports.SceneTopic import SceneTopic
from QuestExports.DialogLine import DialogLine
from QuestExports.BranchDialogs import BranchDialogs
from QuestExports.TopicDialogs import TopicDialogs


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
        # print("Generating Audio Data for file " + file_path)
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
        """
        A Json representation of the object.
        :return:
        """
        obj = Obj2Json()
        obj.add("file_name", self.file_name)
        obj.add("actor_name", self.actor_name)
        obj.add("subtitle", self.subtitle)
        obj.add("quest_id", self.quest_id)
        obj.add("file_path", self.file_path)
        obj.add("dialog_type", self.dialog_type)
        obj.add("emotion", self.emotion)
        obj.add("voice_type", self.voice_type)
        obj.add("topic_id", self.topic_id)
        obj.add("branch_id", self.branch_id)
        obj.add("scene_id", self.scene_id)
        obj.add("scene_phase", self.scene_phase)
        return obj.json()

    def file_path_wav(self):
        return self.file_path + Exts.EXT_WAV

    def file_path_xwm(self):
        return self.file_path + Exts.EXT_XWM

    def file_path_fuz(self):
        return self.file_path + Exts.EXT_FUZ

    @staticmethod
    def generate_list_audio_data(skyrim_path: str, comments_csv: str, actors_csv: str, scene_order_csv: str):
        list_audio_data = []
        list_quest_obj = QuestDialogs.build_quest_objects(skyrim_path, comments_csv, actors_csv, scene_order_csv)
        quest: QuestDialogs
        scene: Scene
        st: SceneTopic
        br: BranchDialogs
        tp: TopicDialogs
        dl: DialogLine
        for quest in list_quest_obj:
            quest_id = quest.quest_name
            scene_phase = -1
            scene_id = ""
            dialog_type = ""
            actor_name = ""
            subtitle = ""
            filepath = ""
            filename = ""
            emotion = ""
            voice_type = ""
            for br in quest.list_branch_dialogs:
                branch_id = br.branch_name
                dialog_type = br.dialog_type
                actor_name = br.actor_name
                for tp in br.list_topic_dialogs:
                    actor_name = tp.actor_name
                    topic_id = tp.topic_name
                    i = 0
                    tpdata_len = tp.get_topic_data_len()
                    while i < tpdata_len:
                        subtitle = tp.get_topic_response(i)
                        emotion = tp.get_topic_mood(i)
                        filepath = tp.get_topic_file_path(i)
                        filename = tp.get_topic_file_name(i)
                        # print("filename:" + filename)
                        # print("filepath:" + filepath)
                        list_audio_data.append(AudioData(file_path=filepath, quest_id=quest_id, actor_name=actor_name,
                                                         subtitle=subtitle, file_name=filename, dialog_type=dialog_type,
                                                         emotion=emotion, voice_type=voice_type, topic_id=topic_id,
                                                         branch_id=branch_id, scene_id=scene_id,
                                                         scene_phase=scene_phase))
                        i += 1
            branch_id = ""
            topic_id = ""
            for scene in quest.list_scenes:
                scene_id = scene.scene_id
                for st in scene.list_scene_topics:
                    dialog_type = st.dialog_type()
                    actor_name = st.actor_name()
                    scene_phase = st.scene_phase()
                    voice_type = st.voice_type()
                    for dl in st.sd_list_dialog_lines:
                        emotion = dl.emotion()
                        filepath = dl.filepath()
                        filename = dl.filename()
                        subtitle = dl.dialogue()
                        list_audio_data.append(
                            AudioData(filepath, quest_id, actor_name, subtitle, filename, dialog_type,
                                      emotion, voice_type, topic_id, branch_id, scene_id, scene_phase))
        return list_audio_data









