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


class AudioWindow:

    DEFAULT_INIT_PROGRESS = "0:00"
    DEFAULT_END_PROGRESS = ""
    DEFAULT_CURRENT_TRACK = ""

    def __init__(self):
        # set window theme
        sg.theme('Default')
        # todo usar dir default
        self.app = AppInfo("..\\App\\")
        # self.app = AppInfo()
        self.audio_logic_layer = AudioLogicLayer()
        self.data = []
        self.current_row = -1

    def run(self, list_audio_data):
        # Load table data
        # todo comentar linha de teste
        list_audio_data = create_audio_list()
        # list_audio_data = self.audio_logic_layer.generate_list_audio_data()
        self.data = AudioWindow.create_audio_table(list_audio_data, 4)

        # table elements
        table_headings = ["Quest ID", "Actor", "Subtitles"]

        # Player Elements
        #slider_volume = sg.Slider(range=(0, 100), key='key_slider_volume', orientation='h', size=(20, 10), default_value=80,
        #                          enable_events=True, tooltip="Volume")
        #
        #slider_progress = [sg.Text(AudioWindow.DEFAULT_INIT_PROGRESS, key="key_text_init_time"),
        #                   sg.Text(AudioWindow.DEFAULT_END_PROGRESS, key="key_text_end_time"),
        #                   sg.Slider(range=(0, 100), key='key_slider_progress', orientation='h', size=(80, 10),
        #                             default_value=70, enable_events=True, tooltip="Progress")]

        track_information = [sg.Text(""), sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')]
        track_sliders = [sg.Button(emojize(":arrow_forward:Play", language='alias'), key="key_play_button"),
                         sg.Button(emojize("\u23F8\uFE0F     Pause", variant='emoji_type'),
                                   key="key_pause_button"),
                         sg.Button(emojize(":stop_button:     Stop", variant='emoji_type'),
                                   key="key_stop_button"),
                         sg.VerticalSeparator(),
                         sg.Slider(range=(0, 100), key='key_slider_volume', orientation='h', size=(20, 10),
                                   default_value=80, enable_events=True, tooltip="Volume"),
                         sg.VerticalSeparator(),
                         sg.Text(AudioWindow.DEFAULT_INIT_PROGRESS, key="key_text_init_time"),
                         sg.Slider(range=(0, 100), key='key_slider_progress', orientation='h', size=(80, 10),
                                   default_value=70, enable_events=True, tooltip="Progress"),
                         sg.Text(AudioWindow.DEFAULT_END_PROGRESS, key="key_text_end_time")]
        tool_box = [sg.Button(emojize(":file_folder:     Open Folder", variant='emoji_type'), key="key_open_button"),
                    sg.Button(emojize(":sparkle:Copy Track Name", language='alias'), key="key_copy_name_button"),
                    sg.Button(emojize(":speech_balloon:    Track Info Details", language='alias'),
                              key="key_copy_info_button"),
                    sg.Button(emojize(":musical_note:     Generate XWM", language='alias'), key="key_gen_xwm_button"),
                    sg.Button(emojize(":studio_microphone:Generate FUZ", language='alias'), key="key_gen_fuz_button"),
                    sg.Button(emojize(":headphones:     UnFUZ", language='alias'), key="key_unfuz_button")],

        # ------ Window Layout ------
        layout = [[sg.Table(values=self.data[1:][:], headings=table_headings,
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
                  [sg.Text(lorem_ipsum, size=(120, None))],
                  track_sliders,
                  [sg.Text('')],
                  [sg.HorizontalSeparator()],
                  [sg.Text(''), sg.Text('Tools')],
                  tool_box,
                  [sg.Multiline(size=(170, 5), enter_submits=False, key='-QUERY-', do_not_clear=False,
                                write_only=True)],
                  [sg.Text(''),
                   sg.Sizegrip()]]

        # ------ Create Window ------
        window = sg.Window('The Table Element', layout,
                           ttk_theme='clam',
                           resizable=False)

        # ------ Event Loop ------
        while True:
            event, values = window.read()
            print(event, values)
            if event == sg.WIN_CLOSED:
                break
            if event == 'Play':
                #for i in range(1, len(self.data)):
                #    self.data.append(self.data[i])
                #window['-TABLE-'].update(values=self.data[1:][:])
                print("Play")
            if event == 'Stop':
                print("Stop")
            if event == 'Open Folder':
                print("Open Folder")
            if event == 'Track Info Details':
                print("Track Info Details")
            if event == "Generate XWM":
                print("Generate XWM")
            if event == "Generete FUZ":
                print("Generete FUZ")
            if event == 'UnFuz':
                print("UnFuz")

            if isinstance(event, tuple):
                # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
                self.current_row = AudioWindow.clicked_row(event)
                print(" -- Clicked Row: " + str(AudioWindow.clicked_row(event)))
                if event[0] == '-TABLE-':
                    if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                        col_num_clicked = event[2][1]
                        new_table = AudioWindow.sort_table(self.data[1:][:], (col_num_clicked, 0))
                        window['-TABLE-'].update(new_table)
                        self.data = [self.data[0]] + new_table
                    window['-CLICKED-'].update(f'{event[2][0]},{event[2][1]}')
        window.close()

    @staticmethod
    def create_audio_table(audio_list, repeat=0):
        al = []
        i = 0
        while i < repeat:
            al.extend(audio_list)
            i += 1
        table = [[ audio.quest_id, audio.actor_name, audio.subtitle] for audio in al]
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



if __name__ == '__main__':
    window = AudioWindow()
    audio_data = create_audio_list()
    window.run(audio_data)

