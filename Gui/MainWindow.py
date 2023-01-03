import PySimpleGUI as sg
from emoji import emojize
from PyUtils.Logger import Logger
from PyUtils.ScreenInfo import ScreenInfo
from Settings.AppInfo import AppInfo
from Settings.ProfileManager import ProfileManager
from Gui.MainLogicLayer import MainLogicLayer
from Gui.ProfilesWindow import ProfilesWindow


class MainWindow:
    """
    Main window class.
    """
    # Style
    WINDOW_HIGH = 550
    WINDOW_SIZE = ScreenInfo.golden_display_pair(WINDOW_HIGH)
    FONT_TEXT = ('MS Sans Serif', 10, 'bold')
    FONT_TITLE2 = ('Any', 14)
    FONT_TITLE1 = ('Any', 18,)
    FONT_SKIPLINE1 = ('Any', 20,)
    FONT_SKIPLINE2 = ('Any', 15,)
    # Application Setup
    BTN_SETTINGS = "Settings"
    BTN_PROFILES = "Profiles"
    BTN_THEME = "Choose Theme"
    BTN_ABOUT = "About"
    BTN_LICENSE = "License"
    # Documentation Generation
    # BTN_IMPORT_FROM_CK = "Import Objects from Creation Kit"
    BTN_IMPORT_FROM_CK = "Import files from Creation Kit"
    BTN_EDIT_SCENES = "Edit Scene Order"
    BTN_EDIT_ACTORS = "Edit Actor's Names"
    BTN_EDIT_COMMENTS = "Edit Comments"
    BTN_DOC_GEN = "Generate Documentation"
    BTN_AUDIO_MANAGER = "Audio Manager Tools"
    # Help
    BTN_TUTORIAL = "Tutorial"
    BTN_GITHUB = "Github"
    BTN_NEXUS = "Nexus"
    # return code
    RET_SUCCESS = 0
    RET_ERROR = 1
    RET_RESTART = 2


    def run(self):
        """
        Run main window.
        :return: void
        """
        #
        # Initialize application
        #
        cd_dialog_docgen = MainLogicLayer()
        _log = Logger.get()
        app = AppInfo()
        str_theme = app.settings_obj.app_theme
        _log.debug("* selected theme: " + str_theme)
        profile_name = cd_dialog_docgen.get_profile_name()
        #
        # Create Windows
        #
        sg.theme(str_theme)
        layout_title_main = [
            sg.Text(emojize(":fleur-de-lis: " + app.APP_NAME_LARGE +" :fleur-de-lis:", variant="emoji_type"),
                    font=('Any', 32))]
        layout_title_config = [
            sg.Text(emojize(f":hammer_and_wrench:Application Settings [Profile: {profile_name}]", variant="emoji_type"), font=MainWindow.FONT_TITLE2)]
        layout_title_export = [
            sg.Text(emojize(":scroll:     Content Manager", variant="emoji_type"), font=MainWindow.FONT_TITLE2)]
        layout_title_help = [
            sg.Text(emojize(":globe_with_meridians:     Help", variant="emoji_type"), font=MainWindow.FONT_TITLE2)]
        # Buttons
        layout_settings = [sg.Button(MainWindow.BTN_SETTINGS),
                           sg.Button(MainWindow.BTN_PROFILES),
                           sg.Button(MainWindow.BTN_THEME),
                           sg.Button(MainWindow.BTN_ABOUT),
                           sg.Button(MainWindow.BTN_LICENSE)]
        layout_export_l1 = [sg.Text("Step 1: Import Objects                "),
                            sg.Button(MainWindow.BTN_IMPORT_FROM_CK)]
        layout_export_l2 = [sg.Text("Step 2: Edit                                "),
                            sg.Button(MainWindow.BTN_EDIT_ACTORS),
                            sg.Button(MainWindow.BTN_EDIT_COMMENTS),
                            sg.Button(MainWindow.BTN_EDIT_SCENES)]
        layout_export_l3 = [sg.Text("Step 3: Manage Quest Content    "),
                            sg.Button(MainWindow.BTN_DOC_GEN), sg.Button(MainWindow.BTN_AUDIO_MANAGER)]
        layout_tutorial = [sg.Button(MainWindow.BTN_TUTORIAL), sg.Button(MainWindow.BTN_GITHUB),
                           sg.Button(MainWindow.BTN_NEXUS)]
        # Layout
        layout = [layout_title_main, [sg.Text("", font=MainWindow.FONT_SKIPLINE1)],
                  layout_title_config, layout_settings, [sg.Text("", font=MainWindow.FONT_SKIPLINE2)],
                  layout_title_export, layout_export_l1, layout_export_l2, layout_export_l3, [sg.Text("", font=MainWindow.FONT_SKIPLINE2)],
                  layout_title_help, layout_tutorial, [sg.Text("", font=MainWindow.FONT_SKIPLINE2)],
                  ]
        window = sg.Window(title=app.label_main_window, layout=layout, size=MainWindow.WINDOW_SIZE,
                           icon=app.app_icon_ico)
        reload = False
        ret_code = MainWindow.RET_SUCCESS
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                break
            # Application Setup
            elif event == MainWindow.BTN_SETTINGS:
                _log.debug("event:" + event)
                cd_dialog_docgen.open_settings_window()
                app.reload()
            elif event == MainWindow.BTN_PROFILES:
                _log.debug("event:" + event)
                ret = cd_dialog_docgen.open_profile_window()
                if ret == ProfilesWindow.RET_RESTART:
                    reload = True
                    break
            elif event == MainWindow.BTN_THEME:
                _log.debug("event:" + event)
                selected_theme = cd_dialog_docgen.open_theme_picker()
                if selected_theme != "":
                    sg.theme(selected_theme)
            elif event == MainWindow.BTN_ABOUT:
                _log.debug("event:" + event)
                cd_dialog_docgen.open_about_window()
            elif event == MainWindow.BTN_LICENSE:
                _log.debug("event:" + event)
                cd_dialog_docgen.open_license_window()
            # Documentation Generation
            elif event == MainWindow.BTN_IMPORT_FROM_CK:
                _log.debug("event:" + event)
                cd_dialog_docgen.import_from_creation_kit()
            elif event == MainWindow.BTN_EDIT_SCENES:
                _log.debug("event:" + event)
                cd_dialog_docgen.open_scenes_editor()
            elif event == MainWindow.BTN_EDIT_ACTORS:
                _log.debug("event:" + event)
                cd_dialog_docgen.open_actors_editor()
            elif event == MainWindow.BTN_EDIT_COMMENTS:
                _log.debug("event:" + event)
                cd_dialog_docgen.open_comments_editor()
            elif event == MainWindow.BTN_DOC_GEN:
                _log.debug("event:" + event)
                cd_dialog_docgen.generate_documentation()
            elif event == MainWindow.BTN_AUDIO_MANAGER:
                _log.debug("event:" + event)
                cd_dialog_docgen.launch_audio_manager()
            # Help
            elif event == MainWindow.BTN_TUTORIAL:
                _log.debug("event:" + event)
                cd_dialog_docgen.open_tutorial()
            elif event == MainWindow.BTN_GITHUB:
                _log.debug("event:" + event)
                cd_dialog_docgen.open_github()
            elif event == MainWindow.BTN_NEXUS:
                _log.debug("event:" + event)
                cd_dialog_docgen.open_nexus()

        if reload:
            ret_code = MainWindow.RET_RESTART
        window.close()

        return ret_code





