import logging

class Logger :
    """"""

    @staticmethod
    def get_logger(level_log=logging.DEBUG, level_console=logging.WARNING, log_file='./App/Logs/ck-dialog-docgen.log'):

        logger = logging.getLogger('PyPro')
        logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        fh = logging.FileHandler('./App/Logs/ck-dialog-docgen.log')
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)

        # create formatter and add it to the handlers
        fhFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        chFormatter = logging.Formatter('%(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s')
        fh.setFormatter(fhFormatter)
        ch.setFormatter(chFormatter)

        # add the handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)

        logger.info("-----------------------------------")
        logger.info("Log system successfully initialised")
        logger.info("-----------------------------------")

        return logger