from emoji import emojize
import PySimpleGUI as sg
from PyUtils.Logger import Logger
from PyUtils.ScreenInfo import ScreenInfo
from Gui.AppInfo import AppInfo


class AboutWindow:

    # FI = 1.618
    WINDOW_HEIGHT = 350
    WINDOW_SIZE = ScreenInfo.golden_display_pair(WINDOW_HEIGHT)
    FONT_TITLE2 = ('Any', 11)
    FONT_TITLE1 = ('Any', 14,)
    FONT_SKIPLINE1 = ('Any', 20,)
    FONT_SKIPLINE2 = ('Any', 15,)
    BTN_OK = "OK"

    def __init__(self, app_dir: str):
        self._log = Logger.get()
        self.app = AppInfo(app_dir)

    def run(self):
        layout_title = [
            sg.Text(emojize(":fleur-de-lis: CK -- Quest Dialog Manager :fleur-de-lis:", variant="emoji_type"),
                font=AboutWindow.FONT_TITLE1)]
        layout_version = [
            sg.Text(self.app.app_version, font=AboutWindow.FONT_TITLE2)]
        layout_about = [
            sg.Text(emojize("CK QuestDialogManages is a tool to help manage your quest mod:\n" +
                            "  *  Allows the conversion and generation of many audio\n" +
                            "     files formats (wav, xwm, fuz)\n" +
                            "  *  Allow you easily manage the audios from you mod: listen\n" +
                            "     to audios, manage file names,and check subtitles;\n" +
                            "  *  Generate beautifull and comprehensive documentation;\n" +
                            "  *  Reusable Comments and anotations for your documentation.\n" +
                            "     Regenerate as many times you want with no loss.\n",
                            variant="emoji_type"),
                    font=AboutWindow.FONT_TITLE2)]
        layout_skipline1 = [sg.Text("", font=AboutWindow.FONT_SKIPLINE2)]
        layout_skipline2 = [sg.Text("", font=AboutWindow.FONT_SKIPLINE2)]
        layout_btn_ok = [sg.Button(AboutWindow.BTN_OK)]
        layout = [layout_title,
                  layout_version,
                  layout_skipline1,
                  layout_about,
                  layout_btn_ok,
                  ]
        window = sg.Window(title=self.app.label_main_window, layout=layout, size=AboutWindow.WINDOW_SIZE,
                           icon=self.app.app_icon_ico)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                break
            if event == AboutWindow.BTN_OK:
                break
        window.close()


if __name__ == '__main__':
    about = AboutWindow("..\\App\\")
    about.run()