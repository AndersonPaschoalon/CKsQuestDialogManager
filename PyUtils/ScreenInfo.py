import ctypes


class ScreenInfo:

    @staticmethod
    def screen_resolution():
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
        return screensize

