import PySimpleGUI as sg
import random
import string
import operator
from emoji import emojize
import emoji
import textwrap
from Gui.AppInfo import AppInfo
from Gui.AudioLogicLayer import AudioLogicLayer
from Gui.AudioData import AudioData
from Gui.TestData import *
import datetime


class AudioWindow:

    # window size
    FI = 1.618
    WINDOW_HIGH = 650
    WINDOW_WIDTH = int(WINDOW_HIGH * FI)
    WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HIGH)
    SUBTITLE_SIZE = int(WINDOW_HIGH/5.5)
    # default values
    DEFAULT_INIT_PROGRESS = "0:00"
    DEFAULT_END_PROGRESS = ""
    DEFAULT_CURRENT_TRACK = ""
    # Text
    KEY_TEXT_CURRENT_TRACK = "key_text_current_track"
    KEY_TEXT_CURRENT_SUBTITLE = "key_text_current_subtitle"
    KEY_TEXT_INIT_TIME = "key_text_init_time"
    KEY_TEXT_END_TIME = "key_text_end_time"
    # Button
    KEY_PLAY_BUTTON = "key_play_button"
    KEY_PAUSE_BUTTON = "key_pause_button"
    KEY_STOP_BUTTON = "key_stop_button"
    KEY_OPEN_BUTTON = "key_open_button"
    KEY_COPY_NAME_BUTTON = "key_copy_name_button"
    KEY_COPY_INFO_BUTTON = "key_copy_info_button"
    KEY_GEN_XWM_BUTTON = "key_gen_xwm_button"
    KEY_GEN_FUZ_BUTTON = "key_gen_fuz_button"
    KEY_UNFUZ_BUTTON = "key_unfuz_button"
    # Slider
    KEY_SLIDER_VOLUME = "key_slider_volume"
    KEY_SLIDER_PROGRESS = "key_slider_progress"


    def __init__(self, app_dir: str):
        # set window theme
        sg.theme('Default')
        self.app = AppInfo(app_dir)
        self.audio_logic_layer = AudioLogicLayer(app_dir)
        self.data = []
        self.current_row = -1
        self.current_track = ""
        self.current_subtitle = ""

    def update_current_track(self, sound, subtitle):
        if not sound == "":
            self.current_track = str(sound)
            self.current_subtitle = str(subtitle)

    def run(self):
        # Load table data
        # todo comentar linha de teste
        list_audio_data = create_audio_list2()
        # for audio in list_audio_data:
        #    print(audio.to_string())
        # TODO use the command below, instead the above
        # list_audio_data = self.audio_logic_layer.generate_list_audio_data()
        self.data = AudioWindow.create_audio_table(list_audio_data, 4)
        # table elements
        table_headings = ["Quest ID", "Actor", "Subtitles"]
        # Player Elements
        track_information = [sg.Text(emojize(":radio:     ")), sg.Text('Audio Track:'), sg.Text("", key=AudioWindow.KEY_TEXT_CURRENT_TRACK)]
        track_sliders = [sg.Button(emojize(":arrow_forward:Play", language='alias'), key=AudioWindow.KEY_PLAY_BUTTON),
                         sg.Button(emojize("\u23F8\uFE0F     Pause", variant='emoji_type'),
                                   key=AudioWindow.KEY_PAUSE_BUTTON),
                         sg.Button(emojize(":stop_button:     Stop", variant='emoji_type'),
                                   key=AudioWindow.KEY_STOP_BUTTON),
                         sg.VerticalSeparator(),
                         sg.Slider(range=(0, 100), key=AudioWindow.KEY_SLIDER_VOLUME, orientation='h', size=(20, 10),
                                   default_value=80, enable_events=True, tooltip="Volume"),
                         sg.VerticalSeparator(),
                         sg.Text(AudioWindow.DEFAULT_INIT_PROGRESS, key=AudioWindow.KEY_TEXT_INIT_TIME),
                         sg.Slider(range=(0, 100), key=AudioWindow.KEY_SLIDER_PROGRESS, orientation='h', size=(80, 10),
                                   default_value=70, enable_events=True, tooltip="Progress"),
                         sg.Text(AudioWindow.DEFAULT_END_PROGRESS, key=AudioWindow.KEY_TEXT_END_TIME)]
        tool_box = [sg.Button(emojize(":file_folder:     Open Folder", variant='emoji_type'), key=AudioWindow.KEY_OPEN_BUTTON),
                    sg.Button(emojize(":sparkle:Copy Track Name", language='alias'), key=AudioWindow.KEY_COPY_NAME_BUTTON),
                    sg.Button(emojize(":speech_balloon:    Track Info Details", language='alias'),
                              key="key_copy_info_button"),
                    sg.Button(emojize(":musical_note:     Generate XWM", language='alias'), key=AudioWindow.KEY_GEN_XWM_BUTTON),
                    sg.Button(emojize(":studio_microphone:Generate FUZ", language='alias'), key=AudioWindow.KEY_GEN_FUZ_BUTTON),
                    sg.Button(emojize(":headphones:     UnFUZ", language='alias'), key=AudioWindow.KEY_UNFUZ_BUTTON)],
        # ------ Window Layout ------
        layout = [[sg.Table(values=self.data[:][:], # values=self.data[1:][:],
                            headings=table_headings,
                            auto_size_columns=True,
                            max_col_width=100,
                            display_row_numbers=False,
                            justification='left',
                            size=(150, 150),
                            num_rows=20,
                            key='-TABLE-',
                            selected_row_colors='red on yellow',
                            enable_events=True,
                            expand_x=True,
                            expand_y=True,
                            enable_click_events=True,  # Comment out to not enable header and other clicks
                            tooltip='Audio list')],
                  [sg.HorizontalSeparator()],
                  track_information,
                  [sg.Text("", size=(AudioWindow.SUBTITLE_SIZE, None), key=AudioWindow.KEY_TEXT_CURRENT_SUBTITLE)],
                  track_sliders,
                  [sg.Text('')],
                  [sg.HorizontalSeparator()],
                  [sg.Text(emojize(":desktop_computer:").strip()), sg.Text('System & Tools')],
                  tool_box,
                  [sg.Multiline(size=(170, 5), enter_submits=False, key='-QUERY-', do_not_clear=False,
                                write_only=True)],
                  [sg.Text(''),
                   sg.Sizegrip()]]
        # ------ Create Window ------
        window = sg.Window('The Table Element',
                           layout,
                           ttk_theme='clam',
                           resizable=False,
                           size=AudioWindow.WINDOW_SIZE)
        # ------ Event Loop ------
        while True:

            # Handle events
            event, values = window.read(timeout=500)
            if isinstance(event, tuple):
                # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
                self.current_row = AudioWindow.clicked_row(event)
                self.update_current_track(self.get_filename(self.current_row), self.get_subtitle(self.current_row))
                if event[0] == '-TABLE-':
                    if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                        col_num_clicked = event[2][1]
                        new_table = AudioWindow.sort_table(self.data[1:][:], (col_num_clicked, 0))
                        window['-TABLE-'].update(new_table)
                        self.data = [self.data[0]] + new_table
                    window[AudioWindow.KEY_TEXT_CURRENT_TRACK].update(self.current_track)
                    window[AudioWindow.KEY_TEXT_CURRENT_SUBTITLE].update(self.current_subtitle)
            # todo debug
            # print("event:<" + str(event) + ">, values:<" + str(values) + ">")

            # self.update_current_track(self.current_track, self.current_subtitle)
            if event == sg.WIN_CLOSED:
                print("Pressed button: sg.WIN_CLOSED")
                break
            if event == AudioWindow.KEY_PLAY_BUTTON:
                print("Pressed button: " + AudioWindow.KEY_PLAY_BUTTON)
                self.audio_logic_layer.play_sound(self.current_track)
            if event == AudioWindow.KEY_STOP_BUTTON:
                print("Pressed button: " + AudioWindow.KEY_STOP_BUTTON)
                self.audio_logic_layer.stop_sound()
            if event == AudioWindow.KEY_PAUSE_BUTTON:
                print("Pressed button: " + AudioWindow.KEY_PAUSE_BUTTON)
                self.audio_logic_layer.pause_sound()
            if event == AudioWindow.KEY_SLIDER_VOLUME:
                print("Pressed button: " + AudioWindow.KEY_SLIDER_VOLUME)
                self.audio_logic_layer.set_volume(values[AudioWindow.KEY_SLIDER_VOLUME])
            if event == AudioWindow.KEY_OPEN_BUTTON:
                print("Pressed button: " + AudioWindow.KEY_OPEN_BUTTON)
                self.audio_logic_layer.open_folder(self.current_track)
            if event == AudioWindow.KEY_COPY_NAME_BUTTON:
                print("Pressed button: " + AudioWindow.KEY_COPY_NAME_BUTTON)
                self.audio_logic_layer.copy_track_name(self.current_track)
            if event == AudioWindow.KEY_COPY_INFO_BUTTON:
                print("Pressed button: " + AudioWindow.KEY_COPY_INFO_BUTTON)
                self.audio_logic_layer.copy_track_info(self.current_track, list_audio_data)
            if event == AudioWindow.KEY_GEN_XWM_BUTTON:
                print("Pressed button: " + AudioWindow.KEY_GEN_XWM_BUTTON)
                self.audio_logic_layer.audio_gen_xwm(self.current_track)
            if event == AudioWindow.KEY_GEN_FUZ_BUTTON:
                print("Pressed button: " + AudioWindow.KEY_GEN_FUZ_BUTTON)
                self.audio_logic_layer.audio_gen_fuz(self.current_track)
            if event == AudioWindow.KEY_UNFUZ_BUTTON:
                print("Pressed button: " + AudioWindow.KEY_UNFUZ_BUTTON)
                self.audio_logic_layer.audio_unfuz(self.current_track)

            # update progress bar
            audio_prog = self.audio_logic_layer.get_current_track_progress()
            audio_len = self.audio_logic_layer.get_current_track_len()
            if audio_len == 0:
                audio_len = 1
            # debug
            # print("Current progress is " + str(audio_prog) + "/" + str(audio_len) + " for " + self.current_track)
            window[AudioWindow.KEY_SLIDER_PROGRESS].update(value=audio_prog, range=(0, audio_len))
            window[AudioWindow.KEY_TEXT_END_TIME].update(value=AudioWindow.sec_to_min(audio_len))

        window.close()



    @staticmethod
    def sec_to_min(sec: int):
        return str(datetime.timedelta(seconds=sec))

    @staticmethod
    def create_audio_table(audio_list, repeat=0):
        """
        Creates an data table to be displayed in the main windows.
        Each row is composed of the following data:
        0 - Quest ID
        1 - Actor Name
        3 - Subtitle
        4 - File Name
        5 - File Path
        :param audio_list:
        :param repeat:
        :return:
        """
        al = []
        i = 0
        while i < repeat:
            al.extend(audio_list)
            i += 1
        audio: AudioData
        table = [[audio.quest_id, audio.actor_name, audio.subtitle, audio.file_name, audio.file_path] for audio in al]
        print(table)
        return table

    @staticmethod
    def clicked_row(event):
        try:
            return event[2][0]
        except:
            return 0

    @staticmethod
    def sort_table(table, cols):
        """ sort a table by multiple columns
            table: a list of lists (or tuple of tuples) where each inner list
                   represents a row
            cols:  a list (or tuple) specifying the column numbers to sort by
                   e.g. (1,0) would sort by column 1, then by column 0
        """
        for col in reversed(cols):
            try:
                table = sorted(table, key=operator.itemgetter(col))
            except Exception as e:
                sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
        return table

    def get_filename(self, clicked_row: int):
        try:
            return self.data[clicked_row][4]
        except:
            return ""

    def get_subtitle(self, clicked_row: int):
        try:
            return self.data[clicked_row][2]
        except:
            return ""






if __name__ == '__main__':
    window = AudioWindow("..\\App\\")
    audio_data = create_audio_list()
    window.run()

