import logging


class _PBLogHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        fmt = '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
        format_date = '%m/%d/%Y %I:%M:%S %p'
        formatter = logging.Formatter(fmt, format_date)
        self.setFormatter(formatter)


class PBLogger:
    def __init__(self, name):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(_PBLogHandler())

    # Imitating logger object functionality

    def set_level(self, level):
        self._logger.setLevel(level)

    def debug(self, s):
        self._logger.debug(s)

    def info(self, s):
        self._logger.info(s)

    def warning(self, s):
        self._logger.warning(s)

    def error(self, s):
        self._logger.error(s)

    def critical(self, s):
        self._logger.critical(s)
