
class AudioLogicLayer:

    def __init__(self):
        print("ok")

    def generate_list_audio_data(self):
        """
        Generates the list of audio data used to fill the AudioWindow table.
        :return:
        """
        list_audio_data = []
        skyrim_path = self.app.settings_obj.skyrim_path
        comments_csv = self.app.settings_obj.comments_file
        actors_csv = self.app.settings_obj.actors_file
        scene_order_csv = self.app.settings_obj.scene_order_file
        docs_dir = self.app.settings_obj.docgen_dir
        # todo
        return list_audio_data

    def play_sound(self, sound_path: str):
        """
        Screen Element: Play Button
        :param sound_path:
        :return:
        """
        self._generate_wav_if_not_exit(sound_path)
        print("todo")


    def play_info(self):
        """
        Screen Element: song progress bar.
        Used to update the screen with the song information in realtime.
        :return:
        """
        is_song_playing = False
        song_position = 12.2
        file_name = ""
        return [is_song_playing, file_name, song_position]

    def set_volume(self, volume: int):
        """
        Screen Element: Volume bar.
        :param volume:
        :return:
        """
        print("todo")

    def open_folder(self, sound_path: str):
        """
        Screen Element: Open Folder Button
        :param sound_path:
        :return:
        """
        print("todo")

    def copy_track_name(self, sound_path: str):
        print("todo")

    def copy_track_info(self, sound_path: str):
        print("todo")

    def audio_gen_xwm(self, sound_path: str):
        print("todo")

    def audio_gen_fuz(self, sound_path: str):
        print("todo")

    def audio_unfuz(self, sound_path: str):
        print("todo")

    def _generate_wav_if_not_exit(self, file_name):
        print("todo")