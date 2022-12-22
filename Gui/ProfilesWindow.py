from emoji import emojize
import PySimpleGUI as sg
from PyUtils.Logger import Logger
from PyUtils.ScreenInfo import ScreenInfo
from Settings.AppInfo import AppInfo
from Settings.ProfileManager import ProfileManager
from Settings.Profile import Profile


class ProfilesWindow:

    # FI = 1.618
    WINDOW_HEIGHT = 350
    WINDOW_SIZE = ScreenInfo.golden_display_pair(WINDOW_HEIGHT)
    FONT_TITLE2 = ('Any', 11)
    FONT_TITLE1 = ('Any', 14,)
    FONT_SKIPLINE1 = ('Any', 20,)
    FONT_SKIPLINE2 = ('Any', 15,)
    # button names
    BTN_NEW = "New"
    BTN_LOAD = "Load"
    BTN_EDIT = "Edit"
    BTN_DELETE = "Delete"
    BTN_EXIT = "Exit"
    # strings
    ACTIVE_STR = "==>"
    # keys
    KEY_BUTTON_MOVE_UP = "key-btn-move-up"
    KEY_BUTTON_MOVE_DOWN = "key-btn-move-down"
    KEY_TABLE_TUPLE_DIC = "key-table-tuple-dic"

    def __init__(self, app_dir: str):
        self._log = Logger.get()
        self.app = AppInfo(app_dir)
        self.profile_manager = ProfileManager()

    def run(self):
        # Title
        active_profile = self.profile_manager.get_active_profile_name()
        layout_title = [sg.Text("Current Profile: " + active_profile, font=ProfilesWindow.FONT_TITLE1)]

        # Buttons
        layout_buttons = [sg.Button(ProfilesWindow.BTN_NEW),
                          sg.Button(ProfilesWindow.BTN_LOAD),
                          sg.Button(ProfilesWindow.BTN_EDIT),
                          sg.Button(ProfilesWindow.BTN_DELETE),
                          sg.Button(ProfilesWindow.BTN_EXIT)]

        # Profile Table
        table_headings = ["Active", "Profile Name", "Description"]
        data = self._load_profile_data()
        layout_table = [
                        [sg.Table(values=data[:][:],
                            headings=table_headings,
                            auto_size_columns=True,
                            max_col_width=100,
                            display_row_numbers=False,
                            justification='left',
                            num_rows=5,
                            key=ProfilesWindow.KEY_TABLE_TUPLE_DIC,
                            selected_row_colors='red on yellow',
                            enable_events=True,
                            expand_x=True,
                            expand_y=True,
                            enable_click_events=True,
                            tooltip='Profile List')]
                    ]
        layout = [layout_title,
                  layout_table,
                  layout_buttons]

        # Display Window
        window = sg.Window(title=self.app.label_main_window,
                           layout=layout,
                           size=ProfilesWindow.WINDOW_SIZE,
                           icon=self.app.app_icon_ico)

        # Main loop
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == ProfilesWindow.BTN_EXIT:  # if user closes window or clicks cancel
                break
            # Application Setup
            elif event == ProfilesWindow.BTN_NEW:
                self._log.debug("event:" + event)
            elif event == ProfilesWindow.BTN_LOAD:
                self._log.debug("event:" + event)
            elif event == ProfilesWindow.BTN_EDIT:
                self._log.debug("event:" + event)
            elif event == ProfilesWindow.BTN_DELETE:
                self._log.debug("event:" + event)
            if event == ProfilesWindow.KEY_BUTTON_MOVE_UP:
                print("")
            if event == ProfilesWindow.KEY_BUTTON_MOVE_UP:
                print("")

        window.close()

    def _load_profile_data(self):
        ret, list_profiles, msg = self.profile_manager.get_profile_list()
        data = []
        p: Profile
        for p in list_profiles:
            p_line = [ProfilesWindow.ACTIVE_STR if p.active else "",
                      p.name,
                      p.comment]
            data.append(p_line)
        return data


if __name__ == '__main__':
    app_dir = "..\\App\\"
    p = ProfilesWindow(app_dir)
    p.run()
