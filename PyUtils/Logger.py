import logging


class Logger:
    """"""
    LOGGER_NAME = "PyPro"
    FORMAT_CONSOLE = '%(levelname)s - %(message)s'
    FORMAT_LOGFILE = '%(asctime)s - %(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s'
    DEFAULT_LOGGER = "default_logger.log"
    _logger = None

    @staticmethod
    def initialize(log_file, level_log=logging.DEBUG, level_console=logging.WARNING):
        """
        Initializes the singleton object.
        :param log_file: The filename where the logs are going to be saved.
        :param level_log: Log level for the log file.
        :param level_console: Log level for the console.
        :return: None
        """
        Logger._logger = logging.getLogger(Logger.LOGGER_NAME)
        Logger._logger.setLevel(level_log)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(log_file)
        fh.setLevel(level_log)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(level_console)
        # create formatter and add it to the handlers
        fh_formatter = logging.Formatter(Logger.FORMAT_LOGFILE)
        ch_formatter = logging.Formatter(Logger.FORMAT_CONSOLE)
        fh.setFormatter(fh_formatter)
        ch.setFormatter(ch_formatter)
        # add the handlers to logger
        Logger._logger.addHandler(ch)
        Logger._logger.addHandler(fh)
        # init log
        Logger._logger.info("-----------------------------------")
        Logger._logger.info("Log system successfully initialised")
        Logger._logger.info("-----------------------------------")

    @staticmethod
    def get():
        """
        Returns the logger object.
        :return: The logger.
        """
        if Logger._logger is not None:
            pass
        else:
            Logger.initialize(Logger.DEFAULT_LOGGER, logging.DEBUG, logging.WARNING)
        return Logger._logger