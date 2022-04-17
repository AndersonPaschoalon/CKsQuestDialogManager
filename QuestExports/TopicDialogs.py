from PyUtils.Obj2Json import Obj2Json
from PyUtils.Functions import *


class TopicDialogs:
    """
    This class represents a Topic dialog from quest object.
    """

    def __init__(self):
        """Default TopicDialogs constructor."""
        # name of the topic
        self.topic_name = ""
        # additional information
        self.comment = ""
        # Eg.: DSilHand_KylmirShadeSkinner
        self.actor_name = ""
        # Player prompt
        self.player_dialog = ""
        # Form ID
        self.form_id = ""
        # Tuples of NPC topic information
        self._list_topic_data = []

    def to_string(self):
        """
        Build a Json string representation of the object.
        :return: json string.
        """
        obj = Obj2Json()
        obj.add("topic_name", self.topic_name)
        obj.add("actor_name", self.actor_name)
        obj.add("player_dialog", self.player_dialog)
        obj.add("form_id", self.form_id)
        obj.addl("_list_topic_data", self._list_topic_data)
        return obj.json()

    def is_topic_data_empty(self):
        if len(self._list_topic_data) > 0:
            False
        else:
            True

    def add_topic_data(self, index: str, response: str, mood: str, file_path: str, file_name: str):
        """
        Add a tuple of topic information.
        :param index:
        :param response:
        :param mood:
        :param file_path:
        :param file_name:
        :return:
        """
        topic_tuple = (text(index), text(response), text(mood), text(file_path), text(file_name))
        self._list_topic_data.append(topic_tuple)

    def sort(self):
        """Sorts this topic information"""
        self._list_topic_data = sorted(self._list_topic_data, key=lambda tup: tup[0])

    def get_topic_data(self):
        """recover this topic information."""
        sorted_topic_list = sorted(self._list_topic_data, key=lambda tup: tup[0])
        self._list_topic_data = sorted_topic_list
        return sorted_topic_list

    def get_topic_data_len(self):
        """
        Retruns the size of the list of topic data.
        :return:
        """
        return len(self._list_topic_data)

    def get_topic_index(self, position: int):
        """
        Returns the index data at a given position in the topic data.
        :param position:
        :return:
        """
        return self._list_topic_data[position][0]

    def get_topic_response(self, position: int):
        """
        Returns the response data at a given position in the topic data.
        :param position:
        :return:
        """
        return self.get_topic_data()[position][1]

    def get_topic_mood(self, position: int):
        """
        Returns the mood data at a given position in the topic data.
        :param position:
        :return:
        """
        return self.get_topic_data()[position][2]

    def get_topic_file_path(self, position: int):
        """
        Returns the file path data at a given position in the topic data.
        :param position:
        :return:
        """
        return self.get_topic_data()[position][3]

    def get_topic_file_name(self, position: int):
        """
        Returns the file name data at a given position in the topic data.
        :param position:
        :return:
        """
        return self.get_topic_data()[position][4]

    def clear(self):
        """Clear _list_topic_data."""
        self._list_topic_data.clear()
