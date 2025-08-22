import RPi.GPIO as gpio
import time
import threading
from fit_manage_qr_detector.logger import Logger

class GateController:

    GATE_PIN = 7
    SLEEP_TIME = 2

    def __init__(self, logger: Logger):
        self.logger = logger

        # Sync variables
        self.lock = threading.Lock()
        self.accept_code = True

    def init(self):
        try:
            gpio.setmode(gpio.BOARD)
            gpio.setup(self.GATE_PIN, gpio.OUT)
        except Exception as e:
            self.logger.log_error("Error on gpio iniy {}".format(e))

    def open(self):
        """
        Thread-safe: multiple threads can call this, but only one will succeed at a time.
        """
        with self.lock:
            if not self.accept_code:
                return
            self.accept_code = False

        self.logger.log_info("Opening gate....")
        gpio.output(self.GATE_PIN, True)
        time.sleep(self.SLEEP_TIME)
        self.logger.log_info("Closing gate....")
        gpio.output(self.GATE_PIN, False)

        with self.lock:
            self.accept_code = True