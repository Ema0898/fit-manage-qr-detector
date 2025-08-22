import threading
import queue
from concurrent.futures import ThreadPoolExecutor
from fit_manage_qr_detector.logger import Logger
from fit_manage_qr_detector.validator import Validator
from fit_manage_qr_detector.gate import GateController

class DetectorWorker(threading.Thread):
    MAX_WORKERS = 1

    def __init__(self, queue: queue, stop_event: threading.Event, validator: Validator, gate: GateController, logger: Logger):
        super().__init__(daemon=True)
        self.queue = queue
        self.validator = validator
        self.gate = gate
        self.logger = logger
        self.stop_event = stop_event

        self.gate_pool_executor = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)

    def run(self):
        try:
            while True:
                code = self.queue.get()
                if code is None:  # poison pill for shutdown
                    break

                if self.validator.validate(code):
                    self.gate_pool_executor.submit(self.gate.open)  # send task to pool
                else:
                    self.logger.log_info("Unauthorized code")

                self.queue.task_done()
        except Exception as e:
            self.logger.log_error("Error on worker thread {}".format(e))
            self.stop_event.set()
        finally:
            self.stop()

    def stop(self):
        self.queue.put(None)
        self.gate_pool_executor.shutdown(wait=True)
