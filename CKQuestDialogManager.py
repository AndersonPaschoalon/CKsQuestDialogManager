import logging
import traceback
import PySimpleGUI as sg
from PyUtils.Logger import Logger
from Gui.AppInfo import AppInfo
from Gui.MainWindow import MainWindow


def initialize_logger():
    """
    Initializes the logger singleton.
    :return:
    """
    app = AppInfo()
    Logger.initialize(app.log_file, level_log=logging.DEBUG, level_console=logging.INFO)


if __name__ == '__main__':
    initialize_logger()
    _log = Logger.get()
    _log.info("###############################################################################")
    _log.info("# Starting application's MainWindow")
    _log.info("###############################################################################")
    app = MainWindow()
    _log.info("# Running app...")
    try:
        app.run()
    except:
        _log.error("** Error: Exception caught at __main__!")
        _log.error("** Error: " + traceback.format_exc())
    _log.info("# Application finished.")

