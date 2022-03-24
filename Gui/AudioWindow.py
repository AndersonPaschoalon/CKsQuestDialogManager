import PySimpleGUI as sg
import random
import string
import operator
from emoji import emojize
import emoji
import textwrap


lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

def create_audio_list():
    s1 = "I have a 2-dimensional table of data implemented as a list of lists in Python. I would like to sort the data by an arbitrary column. This is a common task with tabular data."
    s2 = "For example, Windows Explorer allows me to sort the list of files by Name, Size, Type, or Date Modified. "
    s3 = "I tried the code from this article, however, if there are duplicate entries in the column being sorted, the duplicates are removed."
    s4 = " This is not what I wanted, so I did some further searching, and found a nice solution from the HowTo/Sorting article on the PythonInfo Wiki. "
    s5 = "This method also uses the built-in sorted() function, as well as the key paramenter, and operator.itemgetter(). "
    s6 = "See section 2.1 and 6.7 of the Python Library Reference for more information.) The following code sorts the table by the second column (index 1)."
    s7 = "Note, Python 2.4 or later is required."
    s8 = "This works well, but I would also like the table to be sorted by column 0 in addition to column 1. In this example, column 1 holds the Last Name and column 0 holds the First Name. I would like the table to be sorted first by Last Name, and then by First Name. Here is the code to sort the table by multiple columns."
    s9 = "The cols argument is a tuple specifying the columns to sort by. The first column to sort by is listed first, the second second, and so on."
    s10 = "An example using Python's groupby and defaultdict to do the same task — posted 2014-10-09"
    s11 = "python enum types — posted 2012-10-10"
    audio_list = []
    audio_list.append(AudioData('audio/01\ -\ Unfinished\ Allegro.mp3', "Angels Cry", "Angra", s1))
    audio_list.append(AudioData('audio/02\ -\ Carry\ On.mp3', "Angels Cry", "Angra", s2))
    audio_list.append(AudioData('audio/03\ -\ Time.mp3', "Angels Cry", "Angra", s3))
    audio_list.append(AudioData('audio/04\ -\ Angels Cry.mp3', "Angels Cry", "Angra", s4))
    audio_list.append(AudioData('audio/05\ -\ Stand Away.mp3', "Angels Cry", "Angra", s5))
    audio_list.append(AudioData('audio/06\ -\ Never Understand.mp3', "Angels Cry", "Angra", s6))
    audio_list.append(AudioData('audio/07\ -\ Wuthering Heights.mp3', "Angels Cry", "Angra", s7))
    audio_list.append(AudioData('audio/08\ -\ Streets Of Tomorrow.mp3', "Angels Cry", "Angra", s8))
    audio_list.append(AudioData('audio/09\ -\ Evil Warning.mp3', "Angels Cry", "Angra", s9))
    audio_list.append(AudioData('audio/10\ -\ Lasting Child.mp3', "Angels Cry", "Angra", s10))
    audio_list.append(AudioData('audio/11\ -\ Rainy Nights.mp3', "Fireworks", "Angra", s11))
    return audio_list

class AudioData:
    def __init__(self, audio_file: str, quest_id, actor_name: str, subtitle: str):
        self.audio_file = audio_file
        self.quest_id = quest_id
        self.actor_name = actor_name
        self.subtitle = subtitle


class AudioWindow:

    def __init__(self):
        sg.theme('Default')

    def run(self, list_audio_data):
        # display matrix
        data = AudioWindow.create_audio_table(list_audio_data, 4)

        # table elements
        table_headings = ["Quest ID", "Actor", "Subtitles"]

        # Player Elements
        slider_volume = sg.Slider(range=(0, 100), key='slider_volume', orientation='h', size=(20, 10), default_value=80,
                                  enable_events=True, tooltip="Volume")

        slider_progress = [sg.Text("0:00"),
                           sg.Text("03:05"),
                           sg.Slider(range=(0, 100), key='_SLIDERv2_', orientation='h', size=(80, 10), default_value=70,
                                     enable_events=True, tooltip="Progress")]

        track_information = [sg.Text(""), sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')]

        emojize(":fleur-de-lis: Play", variant="emoji_type")

        track_sliders = [sg.Button(emojize(":arrow_forward:Play", language='alias')),
                         sg.Button(emojize(":black_medium_square:     Stop", variant='emoji_type')),
                         sg.VerticalSeparator(),
                         sg.Slider(range=(0, 100), key='slider_volume', orientation='h', size=(20, 10),
                                   default_value=80, enable_events=True, tooltip="Volume"),
                         sg.VerticalSeparator(),
                         sg.Text("0:00"),
                         sg.Slider(range=(0, 100), key='_SLIDERv2_', orientation='h', size=(80, 10), default_value=70,
                                   enable_events=True, tooltip="Progress"),
                         sg.Text("03:05")]

        tool_box = [sg.Button(emojize(":file_folder:     Open Folder", variant='emoji_type')),
                    sg.Button(emojize(":sparkle:Copy Track Name", language='alias')),
                    sg.Button(emojize(":speech_balloon:    Track Info Details", language='alias')),
                    sg.Button(emojize(":musical_note:     Generate XWM", language='alias')),
                    sg.Button(emojize(":studio_microphone:Generate FUZ", language='alias')),
                    sg.Button(emojize(":headphones:     UnFUZ", language='alias'))],

        # ------ Window Layout ------
        layout = [[sg.Table(values=data[1:][:], headings=table_headings,
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
                for i in range(1, len(data)):
                    data.append(data[i])
                window['-TABLE-'].update(values=data[1:][:])
            if event == 'Stop':
                print("Stop")
            if event == 'Copy File Name':
                print("Copy File Name")
            if event == "Open Folder":
                print("Open Folder")
            if isinstance(event, tuple):
                # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
                print(" -- Clicked Row: " + str(AudioWindow.clicked_row(event)))
                if event[0] == '-TABLE-':
                    if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                        col_num_clicked = event[2][1]
                        new_table = AudioWindow.sort_table(data[1:][:], (col_num_clicked, 0))
                        window['-TABLE-'].update(new_table)
                        data = [data[0]] + new_table
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

