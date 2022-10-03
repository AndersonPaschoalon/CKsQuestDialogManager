from emoji import emojize
import PySimpleGUI as sg
from PyUtils.Logger import Logger
from PyUtils.ScreenInfo import ScreenInfo
from Settings.AppInfo import AppInfo


class LicenseWindow:

    # FI = 1.618
    WINDOW_HEIGHT = 600
    WINDOW_SIZE = ScreenInfo.golden_display_pair(WINDOW_HEIGHT)
    FONT_TITLE2 = ('Any', 11)
    FONT_TITLE1 = ('Any', 14,)
    FONT_SKIPLINE1 = ('Any', 20,)
    FONT_SKIPLINE2 = ('Any', 15,)
    HLINE = "-----------------------------------------------------------------------------------------------------------"
    BTN_OK = "OK"

    def __init__(self, app_dir: str):
        self._log = Logger.get()
        self.app = AppInfo(app_dir)

    def run(self):
        license_text = ""
        try:
            with open(self.app.license) as f:
                license_text = f.read()
        except:
            self._log.error("Could not read Licence File!")
        layout_title = [
            sg.Text(emojize(":fleur-de-lis: " + self.app.label_main_window + " :fleur-de-lis:", variant="emoji_type"),
                font=LicenseWindow.FONT_TITLE1)]
        layout_version = [
            sg.Text(self.app.app_version, font=LicenseWindow.FONT_TITLE2)]
        layout_license = [
            sg.Text(emojize(str(license_text),
                            variant="emoji_type"),
                    font=LicenseWindow.FONT_TITLE2)]
        layout_skipline1 = [sg.Text("", font=LicenseWindow.FONT_SKIPLINE2)]
        layout_skipline2 = [sg.Text("", font=LicenseWindow.FONT_SKIPLINE2)]
        layout_hline1 = [sg.Text(LicenseWindow.HLINE, font=LicenseWindow.FONT_SKIPLINE2)]
        layout_hline2 = [sg.Text(LicenseWindow.HLINE, font=LicenseWindow.FONT_SKIPLINE2)]
        layout_btn_ok = [sg.Button(LicenseWindow.BTN_OK)]
        layout = [layout_title,
                  layout_version,
                  layout_skipline1,
                  layout_hline1,
                  layout_license,
                  layout_hline2,
                  layout_btn_ok,]
        window = sg.Window(title=self.app.label_main_window, layout=layout, size=LicenseWindow.WINDOW_SIZE,
                           icon=self.app.app_icon_ico)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                break
            if event == LicenseWindow.BTN_OK:
                break
        window.close()


if __name__ == '__main__':
    about = LicenseWindow("..\\App\\")
    about.run()