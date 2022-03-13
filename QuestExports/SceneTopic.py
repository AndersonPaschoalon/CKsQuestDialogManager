from PyUtils.Obj2Json import Obj2Json


class SceneTopic:
    """

    """

    def __init__(self, scene_id, alias, voice_type, scene_phase):
        self.sd_scene_id = scene_id     # SceneDialogue.SCENE
        self.sd_alias = alias        # SceneDialogue.ALIAS
        self.sd_voice_type = voice_type   # SceneDialogue.VOICE TYPE
        self.sd_scene_phase = scene_phase  # SceneDialogue.SCENE PHASE (last)
        self.de_actor_id = ""
        self.sd_list_dialog_lines = []

    def set_dialog_lines(self, list_dialog_lines):
        self.sd_list_dialog_lines = list_dialog_lines

    def set_dialog_export(self, filename_key: str, response_index: int, filepath: str):
        i = 0
        was_set = False
        while i < len(self.sd_list_dialog_lines):
            if self.sd_list_dialog_lines[i].sd_filename == filename_key:
                self.sd_list_dialog_lines[i].set_dialog_export(response_index, filepath)
                was_set = True
            i += 1
        return was_set

    def get_list_filenames_keys(self):
        i = 0
        list_filenames = []
        for dl in self.sd_list_dialog_lines:
            list_filenames.append(dl.sd_filename)
        return list_filenames

    def to_string(self):
        obj = Obj2Json()
        obj.add("sd_scene_id", self.sd_scene_id)
        obj.add("sd_alias", self.sd_alias)
        obj.add("sd_voice_type", self.sd_voice_type)
        obj.add("sd_scene_phase", self.sd_scene_phase)
        obj.add("de_actor_id", self.de_actor_id)
        list_dl_str = []
        for dl in self.sd_list_dialog_lines:
            list_dl_str.append(dl.to_string())
        obj.addl("sd_list_dialog_lines", list_dl_str)
        return obj.json()

    def sort_dialog_lines(self):
        self.sd_list_dialog_lines.sort(key=lambda x: x.de_response_index, reverse=True)

