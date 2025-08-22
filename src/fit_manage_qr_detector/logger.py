import logging
from systemd.journal import JournalHandler

class Logger:
    def __init__(self, name=__name__, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        log_fmt = logging.Formatter("%(levelname)s %(message)s")
        log_ch = JournalHandler()
        log_ch.setFormatter(log_fmt)

        if not self.logger.handlers:  # avoid duplicate handlers
            self.logger.addHandler(log_ch)

    def log_error(self, message):
        print(message)
        self.logger.error(message)

    def log_info(self, message):
        print(message)
        self.logger.info(message)