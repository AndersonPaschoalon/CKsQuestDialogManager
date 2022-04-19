import ctypes


class ScreenInfo:
    FI = 1.618

    @staticmethod
    def screen_resolution():
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
        return screensize

    @staticmethod
    def golder_ratio(height=0):
        return int(height * ScreenInfo.FI)

    @staticmethod
    def golden_display_pair(height=0):
        width = int(height * ScreenInfo.FI)
        height = int(height)
        pair = (width, height)
        return pair

