from typing import List
from PyUtils.Obj2Json import Obj2Json
from .DialogLine import DialogLine


class SceneTopic:
    """
    A SceneTopic is a ordered sequence of phases said by a single character in sequence, inside a Scene.
    """

    def __init__(self, scene_id, alias, voice_type, scene_phase):
        # data from SceneDialog_ file
        self.actor_name = ""
        self.sd_scene_id = scene_id     # SceneDialogue.SCENE
        self.sd_alias = alias        # SceneDialogue.ALIAS
        self.sd_voice_type = voice_type   # SceneDialogue.VOICE TYPE
        self.sd_scene_phase = scene_phase  # SceneDialogue.SCENE PHASE (last)
        self.de_actor_id = ""
        self.de_actor_race = ""
        self.de_dialog_type = ""
        self.sd_list_dialog_lines = []

    def count_dialog_lines(self):
        """
        Count the number of dialog lines.
        :return: number of dialog lines.
        """
        return len(self.sd_list_dialog_lines)

    def set_dialog_lines(self, list_dialog_lines: List[DialogLine]):
        self.sd_list_dialog_lines.clear()
        self.sd_list_dialog_lines.extend(list_dialog_lines[:])

    def set_dialog_export(self, filename_key: str, response_index: int, filepath: str,
                          actor_id: str, actor_race: str, dialog_type: str):
        i = 0
        was_set = False
        while i < len(self.sd_list_dialog_lines):
            if self.sd_list_dialog_lines[i].sd_filename == filename_key:
                self.sd_list_dialog_lines[i].set_dialog_export(response_index, filepath)
                was_set = True
            i += 1
        self.de_actor_id = actor_id
        self.de_actor_race = actor_race
        self.de_dialog_type = dialog_type
        return was_set

    def set_actor_name(self, name: str):
        self.actor_name = name

    def get_actor_id(self):
        return self.de_actor_id

    def get_actor_alias(self):
        return self.sd_alias

    def get_list_filenames_keys(self):
        """
        Return list of filename_keys from current SceneTopic.
        :return:
        """
        list_filenames = []
        for dl in self.sd_list_dialog_lines:
            list_filenames.append(dl.sd_filename)
        return list_filenames

    def get_scene_phase(self):
        """
        Returns the scene_phase of the SceneTopic object.
        :return: the scene phase.
        """
        return self.sd_scene_phase

    def to_string(self):
        """
        Build a Json string representation of the object.
        :return: json string.
        """
        obj = Obj2Json()
        obj.add("actor_name", self.actor_name)
        # SceneDialog_
        obj.add("sd_scene_id", self.sd_scene_id)
        obj.add("sd_alias", self.sd_alias)
        obj.add("sd_voice_type", self.sd_voice_type)
        obj.add("sd_scene_phase", self.sd_scene_phase)
        # dialogExport
        obj.add("de_actor_id", self.de_actor_id)
        obj.add("de_actor_race", self.de_actor_race)
        obj.add("de_dialog_type", self.de_dialog_type)
        list_dl_str = []
        for dl in self.sd_list_dialog_lines:
            list_dl_str.append(dl.to_string())
        obj.addl("sd_list_dialog_lines", list_dl_str)
        return obj.json()

    def sort_dialog_lines(self):
        """
        Sort list of dialog lines.
        :return: void
        """
        self.sd_list_dialog_lines.sort(key=lambda x: x.de_response_index, reverse=False)
