import queue
import threading
from fit_manage_qr_detector.logger import Logger
from fit_manage_qr_detector.gate import GateController
from fit_manage_qr_detector.validator import Validator
from fit_manage_qr_detector.detector import DetectorWorker
from fit_manage_qr_detector.camera import Camera

queue = queue.Queue()
stop_event = threading.Event()

logger = Logger()
gate = GateController(logger)
validator = Validator(logger)
detector_worker = DetectorWorker(queue, stop_event, validator, gate, logger)
camera = Camera(queue, stop_event, logger)

def cleanup():
    logger.log_info("Exiting ...")
    camera.release()
    detector_worker.stop()

def start():
    gate.init()
    detector_worker.start()
    camera.run()

def main():
    try:
        start()
    except KeyboardInterrupt:
        cleanup()
    except Exception:
        cleanup()

if __name__ == "__main__":
    main()
