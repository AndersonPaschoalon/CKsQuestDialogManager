"""
import PySimpleGUI as sg
from emoji import emojize
from CkLogicLayer import CkLogicLayer
from PyUtils.Logger import Logger
from AppInfo import AppInfo

FI = 1.618
WINDOW_HIGH = 500
WINDOW_WIDTH = int(WINDOW_HIGH*FI)
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HIGH)
FONT_TEXT = ('MS Sans Serif', 10, 'bold')
FONT_TITLE2 = ('Any', 14)
FONT_TITLE1 = ('Any', 18,)
FONT_SKIPLINE1 = ('Any', 20,)
FONT_SKIPLINE2 = ('Any', 15,)


if __name__ == '__main__':
    #
    # Initialize application
    #
    cd_dialog_docgen = CkLogicLayer()
    _log = Logger.get()
    app = AppInfo()
    str_theme = app.settings_obj.app_theme
    _log.debug("* selected theme: " + str_theme)
    #
    # Create Windows
    #
    sg.theme(str_theme)
    layout_title_main = [sg.Text(emojize(":fleur-de-lis: CreationKit-DialogDocGen :fleur-de-lis:", variant="emoji_type"), font=('Any', 32))]
    layout_title_config = [sg.Text(emojize(":hammer_and_wrench:Application Setup", variant="emoji_type"), font=FONT_TITLE2)]
    layout_title_export = [sg.Text(emojize(":scroll:     Documentation Generation", variant="emoji_type"), font=FONT_TITLE2)]
    layout_title_help = [sg.Text(emojize(":globe_with_meridians:     Help", variant="emoji_type"), font=FONT_TITLE2)]
    BTN_SETTINGS = "Settings"
    BTN_THEME = "Choose Theme"
    BTN_EXPORT_CSV = "Export Objects to CSV files"
    BTN_DOC_GEN = "Generate Documentation"
    BTN_TUTORIAL = "Tutorial"
    BTN_GITHUB = "Github"
    BTN_NEXUS = "Nexus"
    # Buttons
    layout_settings = [sg.Button(BTN_SETTINGS), sg.Button(BTN_THEME)]
    layout_export = [sg.Button(BTN_EXPORT_CSV), sg.Button(BTN_DOC_GEN)]
    layout_tutorial = [sg.Button(BTN_TUTORIAL), sg.Button(BTN_GITHUB), sg.Button(BTN_NEXUS)]
    # Layout
    layout = [layout_title_main, [sg.Text("", font=FONT_SKIPLINE1)],
              layout_title_config, layout_settings, [sg.Text("", font=FONT_SKIPLINE2)],
              layout_title_export, layout_export, [sg.Text("", font=FONT_SKIPLINE2)],
              layout_title_help, layout_tutorial, [sg.Text("", font=FONT_SKIPLINE2)],
              ]
    window = sg.Window(title="Creation Kit - Dialog Doc Generator", layout=layout, size=WINDOW_SIZE, icon=app.app_icon_ico)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        elif event == BTN_SETTINGS:
            _log.debug("event:" + event)
            cd_dialog_docgen.open_settings_window()
        elif event == BTN_THEME:
            _log.debug("event:" + event)
            selected_theme = cd_dialog_docgen.open_theme_picker()
            if selected_theme != "":
                sg.theme(selected_theme)
        elif event == BTN_EXPORT_CSV:
            _log.debug("event:" + event)
            cd_dialog_docgen.export_objects_to_csv()
        elif event == BTN_DOC_GEN:
            _log.debug("event:" + event)
            cd_dialog_docgen.generate_documentation()
        elif event == BTN_TUTORIAL:
            _log.debug("event:" + event)
            cd_dialog_docgen.open_tutorial()
        elif event == BTN_GITHUB:
            _log.debug("event:" + event)
            cd_dialog_docgen.open_github()
        elif event == BTN_NEXUS:
            _log.debug("event:" + event)
            cd_dialog_docgen.open_nexus()

    window.close()

"""