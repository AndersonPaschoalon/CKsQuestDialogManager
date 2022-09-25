import csv
import PySimpleGUI as sg
from os.path import exists
from PyUtils.CsvDicTuple import CsvDicTuple
from PyUtils.Logger import Logger
from Gui.AppInfo import AppInfo


class CsvReorderWindow:
    """
    This class manager the Csv Reorder Window.
    """

    KEY_BUTTON_MOVE_UP = "key-btn-move-up"
    KEY_BUTTON_MOVE_DOWN = "key-btn-move-down"
    KEY_TABLE_TUPLE_DIC = "key-table-tuple-dic"

    def __init__(self, app_dir: str, csv_delimiter=",", csv_cote_char='"'):
        self.current_row_int = 0
        self.csv_delimiter = csv_delimiter
        self.csv_cote_char = csv_cote_char
        self._log = Logger.get()
        self.app = AppInfo(app_dir)

    def run(self, filename="", label_key="Key", label_value="Value"):
        self._log.debug("CsvReorderWindow.run() filename:" + filename + ", label_key:" + label_key + ", label_value:" +
                        label_value)
        if filename == "":
            popup_text = "File name is empty."
            return
        if not exists(filename):
            popup_text = "File {0} does not exist.".format(filename)
            return
        # print(" -- self.app.app_icon_ico:" + self.app.app_icon_ico)
        dic_tuple = CsvDicTuple(dic_file=filename)
        data = self.load_csv(filename)
        table_headings = [label_key, label_value]
        layout_table = [
                        [sg.Table(values=data[:][:],
                            headings=table_headings,
                            auto_size_columns=True,
                            max_col_width=100,
                            display_row_numbers=False,
                            justification='left',
                            num_rows=5,
                            key=CsvReorderWindow.KEY_TABLE_TUPLE_DIC,
                            selected_row_colors='red on yellow',
                            enable_events=True,
                            expand_x=True,
                            expand_y=True,
                            enable_click_events=True,
                            tooltip='File {0}'.format(filename))],
                        [sg.Button("/\ Move Up", key=CsvReorderWindow.KEY_BUTTON_MOVE_UP),
                         sg.Button("Move Down \/ ", key=CsvReorderWindow.KEY_BUTTON_MOVE_DOWN )]
                    ]
        window = sg.Window(title="CsvReorderWindow [{0}]".format(filename),
                           layout=layout_table,
                           ttk_theme='clam',
                           resizable=False,
                           size=(500, 300),
                           element_justification='c',
                           icon=self.app.app_icon_ico)
        while True:
            # update current row selected
            event, values = window.read(timeout=100000)
            curr_row = self.current_row(event, values)
            if curr_row != self.current_row_int:
                self.current_row_int = curr_row
                self._log.debug("=> curr_row:" + str(curr_row))
                self._log.debug("key:" + str(data[curr_row][0]) + ", value:" + str(data[curr_row][1]))

            if event == sg.WIN_CLOSED:
                self._log.debug("Pressed button: sg.WIN_CLOSED")
                break

            if event == CsvReorderWindow.KEY_BUTTON_MOVE_UP:
                [key, value] = self.get_data_key_value(data)
                dic_tuple.move_up(key, value)
                data = self.load_csv(filename)
                abs_pos = dic_tuple.tuple_absolute_position(key, value)
                if abs_pos >= 0:
                    self.current_row_int = abs_pos
                    self._log.debug("-- [key, value]=" + str([key, value]) + "current_row_int:" + str(self.current_row_int))
                    window[CsvReorderWindow.KEY_TABLE_TUPLE_DIC].update(values=data[:][:], select_rows=[self.current_row_int])
                    window[CsvReorderWindow.KEY_TABLE_TUPLE_DIC].SetFocus(force=True)
                else:
                    popup_txt = ""
                    if abs_pos == -1:
                        popup_txt = "Error: tuple (" + str(key) + ", " + str(value) + ") could not be found!"
                    elif abs_pos == -2:
                        popup_txt = "Exception processing tuple (" + str(key) + ", " + str(value) + ")!"
                    else:
                        popup_txt = "Unknown Error! Return code <" + str(abs_pos) + ">"
                    self._log.debug("abs_pos:" + str(abs_pos) + ", popup_txt:" + popup_txt())

            if event == CsvReorderWindow.KEY_BUTTON_MOVE_DOWN:
                [key, value] = self.get_data_key_value(data)
                dic_tuple.move_down(key, value)
                self.current_row_int = dic_tuple.tuple_absolute_position(key, value)
                data = self.load_csv(filename)
                window[CsvReorderWindow.KEY_TABLE_TUPLE_DIC].update(values=data[:][:], select_rows=[self.current_row_int])
                window[CsvReorderWindow.KEY_TABLE_TUPLE_DIC].SetFocus(force=True)

    def load_csv(self, filename):
        data = []
        with open(filename, "r") as csvfile:
            rd = csv.reader(csvfile, delimiter=",", quotechar='"')
            for row in rd:
                data.append(row)
        return data

    def current_row(self, event, values):
        # print("event:<{0}>, values:<{1}>".format(str(event), str(values)))
        try:
            cur_row = values[CsvReorderWindow.KEY_TABLE_TUPLE_DIC][0]
            return cur_row
        except:
            return self.current_row_int

    def get_data_key_value(self, data):
        key = ""
        value = ""
        try:
            key = data[self.current_row_int][0]
            value = data[self.current_row_int][1]
        finally:
            return [key, value]



if __name__ == '__main__':
    csv_file = "../Sandbox/DicTuple01.csv"
    app_dir = "..\\App\\"
    reorder = CsvReorderWindow(app_dir)
    data = reorder.load_csv(csv_file)
    # print("data:" + str(data))
    reorder.run(csv_file)
