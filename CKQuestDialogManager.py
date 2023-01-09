import logging
import traceback
import multiprocessing
import PySimpleGUI as sg
from PyUtils.Logger import Logger
from Settings.AppInfo import AppInfo, global_app_configuration
from Gui.MainWindow import MainWindow


APP_DIRECTORY = ".\\App\\"

if __name__ == '__main__':
    # multiprocess support
    multiprocessing.freeze_support()
    # global configuration
    global_app_configuration()
    ret_code = 0

    _log = Logger.get()
    _log.info("###############################################################################")
    _log.info("# Starting application's MainWindow")
    _log.info("###############################################################################")
    # main loop
    while True:
        app = MainWindow()
        _log.info("# Running app...")
        try:
            ret_code = app.run()
        except:
            _log.error("** Error: Exception caught at __main__!")
            _log.error("** Error: " + traceback.format_exc())
        _log.info("# Application finished.")
        if ret_code != MainWindow.RET_RESTART:
            break

