from emoji import emojize
import PySimpleGUI as sg
from PyUtils.Logger import Logger
from PyUtils.ScreenInfo import ScreenInfo
from Settings.AppInfo import AppInfo
from Settings.ProfileManager import ProfileManager
from Settings.Profile import Profile


class ProfilesWindow:
    # FI = 1.618
    WINDOW_HEIGHT = 600
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
    BTN_CANCEL = "Cancel"
    BTN_OK = "Ok"
    # strings
    ACTIVE_STR = "===>"
    # keys
    KEY_BUTTON_MOVE_UP = "key-btn-move-up"
    KEY_BUTTON_MOVE_DOWN = "key-btn-move-down"
    # KEY_TABLE_TUPLE_DIC = "key-table-tuple-dic"
    KEY_UP = "Up:38"
    KEY_DOWN = "Down:40"
    # return codes
    RET_SUCCESS = 0
    RET_ERROR = 1
    RET_RESTART = 2

    def __init__(self, app_dir: str):
        self._log = Logger.get()
        self.app = AppInfo(app_dir)
        self.profile_manager = ProfileManager()

    def _load_profile_data(self):
        ret, list_profiles, msg = self.profile_manager.get_profile_list()
        data = []
        p: Profile
        active_profile = ""
        for p in list_profiles:
            p_line = [ProfilesWindow.ACTIVE_STR if p.active else "",
                      p.name,
                      p.comment]
            if p.active:
                active_profile = p.name
            data.append(p_line)
        return data, active_profile

    def _gui_message_box_alert(self, title="", message=""):
        layout = [[sg.Text(title)],
                  [sg.Text("")],
                  [sg.Text(message)],
                  [sg.Button("Ok")]]
        window = sg.Window(title=self.app.label_main_window,
                           layout=layout,
                           icon=self.app.app_icon_ico,
                           return_keyboard_events=True)
        while True:
            event, values = window.read(timeout=500)
            if event == sg.WIN_CLOSED or event == ProfilesWindow.BTN_CANCEL or event == "Ok":
                break
        window.close()

    def _gui_message_box_yes_no(self, title="", message=""):
        ret_val = False
        layout = [[sg.Text(title)],
                  [sg.Text("")],
                  [sg.Text(message)],
                  [sg.Button("Yes"), sg.Text("          "), sg.Button("No")]]
        window = sg.Window(title=self.app.label_main_window,
                           layout=layout,
                           icon=self.app.app_icon_ico,
                           return_keyboard_events=True)
        while True:
            event, values = window.read(timeout=500)
            if event == sg.WIN_CLOSED or event == ProfilesWindow.BTN_CANCEL or event == "No":
                break
            elif event == "Yes":
                ret_val = True
                break
        window.close()
        return ret_val

    def _gui_profile_editor(self, name="", comments=""):
        ret_val = False
        layout = [[sg.Text("Profile Name:"), sg.InputText(default_text=name, key="profile-name")],
                  [sg.Text("Profile Comments:")],
                  [sg.Multiline(size=(65, 8), key="profile-comment", default_text=comments)],
                  [sg.Button("Ok"), sg.Button("Cancel")]]
        window = sg.Window(title=self.app.label_main_window,
                           layout=layout,
                           icon=self.app.app_icon_ico,
                           return_keyboard_events=True)
        while True:
            event, values = window.read(timeout=500)
            if event == sg.WIN_CLOSED or event == ProfilesWindow.BTN_CANCEL:
                break
            # Application Setup
            elif event == ProfilesWindow.BTN_OK:
                ret_val = True
                break
        window.close()
        return ret_val, (values['profile-name'], values['profile-comment'])

    def _create_new_profile(self, current_name, current_comment):
        ret_val, (profile_name, comment) = self._gui_profile_editor(current_name, current_comment)
        if ret_val:
            #print(">>", self._gui_profile_editor(name=current_name, comments=current_comment))
            ret, msg = True, "Success"
            #ret, msg = self.profile_manager.create_profile(profile_name=profile_name, comment=comment)
            if ret:
                self._gui_message_box_alert(title="Success", message=f"Profile {profile_name} created successfully!")
            else:
                err_msg = f"Error creating profile {profile_name}!\n Reason:{msg}"
                self._gui_message_box_alert(title="Error",
                                            message=err_msg)

    def _edit_profile(self, active_profile, current_name, current_comment):
        ret_val, (new_name, new_comment) = self._gui_profile_editor(current_name, current_comment)
        if ret_val:
            #print(">>", self._gui_profile_editor(name=current_name, comments=current_comment))
            if current_name == active_profile and (new_name != current_name or new_comment != current_comment):
                #self.profile_manager.update_profile(new_profile_name=new_name, new_profile_description=new_comment)
                print("self.profile_manager.update_profile()")
            elif new_name != current_name or new_comment != current_comment:
                #self.profile_manager.update_target_profile(target_profile=current_name,
                #                                           new_profile_name=new_name,
                #                                           new_profile_description=new_comment)
                print("self.profile_manager.update_target_profile()")

    def _delete_profile(self, profile_to_delete, active_profile):
        if profile_to_delete == active_profile:
            self._gui_message_box_alert(title="Cannot complete operation.",
                                        message="Active profile cannot be deleted!")
            return True
        ret = self._gui_message_box_yes_no(title=f"Are you SURE you want to DELETE the profile {profile_to_delete}?",
                                           message="**Warning** This operation cannot be undone. Press No to Cancel.")
        if ret:
            # self.profile_manager.delete_profile(profile_name=profile_to_delete)
            print("self.profile_manager.delete_profile(", profile_to_delete, ")")
        return ret

    def _load_profile(self, profile_to_load):
        ret, status = True, "Test"
        # ret, status = self.profile_manager.activate_profile(profile_to_activate=profile_to_load)
        if ret:
            self._gui_message_box_alert(title="Profile Loaded!",
                                        message="The application will be restarted to apply the changes!")
        else:
            self._gui_message_box_alert(title=f"Error Loading Profile {profile_to_load}!",
                                        message=f"Reason:{status}")

    @staticmethod
    def _clicked_profile(event, data):
        row = 0
        try:
            row = int(event[2][0])
        except:
            row = 0
        return data[row][1], data[row][2]

    @staticmethod
    def _moved_profile(values, data):
        row = 0
        try:
            row = int(values['-TABLE-'][0])
        except:
            row = 0
        return data[row][1], data[row][2]

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
        data, active_profile = self._load_profile_data()
        layout_table = [[sg.Table(values=data[:][:],
                                  headings=table_headings,
                                  auto_size_columns=True,
                                  max_col_width=10000,
                                  display_row_numbers=False,
                                  vertical_scroll_only=False,
                                  justification='left',
                                  num_rows=5,
                                  key='-TABLE-',
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
                           icon=self.app.app_icon_ico,
                           return_keyboard_events=True)

        # Main loop
        # Event Loop to process "events" and get the "values" of the inputs
        ret_val = ProfilesWindow.RET_SUCCESS
        current_profile = ""
        current_comment = ""
        while True:

            #
            # Filter selected profile
            #
            event, values = window.read(timeout=500)
            if isinstance(event, tuple):
                # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
                if event[0] == '-TABLE-':
                    current_profile, current_comment = ProfilesWindow._clicked_profile(event, data)
                    print("----------------->> current_profile:", current_profile)
            # event: Down:40 , values: {'-TABLE-': [3]} TestProfile03
            if event == ProfilesWindow.KEY_UP or event == ProfilesWindow.KEY_DOWN:
                current_profile, current_comment = ProfilesWindow._moved_profile(values, data)
                print("============ current_profile:", current_profile)

            #
            # perform the action
            #
            # if user closes window or clicks cancel
            if event == sg.WIN_CLOSED or event == ProfilesWindow.BTN_EXIT:
                break
            # Application Setup
            elif event == ProfilesWindow.BTN_NEW:
                self._log.debug("event:" + event)
                self._create_new_profile(current_name="New_Profile", current_comment="Profile Description")
            elif event == ProfilesWindow.BTN_LOAD:
                self._log.debug("event:" + event)
            elif event == ProfilesWindow.BTN_EDIT:
                self._edit_profile(active_profile=active_profile,
                                   current_name=current_profile,
                                   current_comment=current_comment)
            elif event == ProfilesWindow.BTN_DELETE:
                self._delete_profile(profile_to_delete=current_profile, active_profile=active_profile)
                self._log.debug("event:" + event)
            elif event == ProfilesWindow.BTN_LOAD:
                self._load_profile(profile_to_load=current_profile)


        window.close()
        return ret_val

if __name__ == '__main__':
    app_dir = "App\\"
    p = ProfilesWindow(app_dir)
    p.run()
