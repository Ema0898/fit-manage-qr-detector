import cv2
import queue
import time
import threading
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from fit_manage_qr_detector.logger import Logger

class Camera:
    QR_SCAN_COOLDOWN = 3
    CAMERA_INDEX = 0

    def __init__(self, queue: queue, stop_event: threading.Event, logger: Logger):
        self.queue = queue
        self.logger = logger
        self.stop_event = stop_event

        self.last_code = None
        self.last_time = 0
        self.cap = None
        self.stop = False

    def run(self):
        try:
            self.cap = cv2.VideoCapture(self.CAMERA_INDEX)

            if not self.cap.isOpened():
                raise RuntimeError("Cannot open camera")

            self.logger.log_info("Camera opened successfully")

            while self.cap.isOpened() and not self.stop_event.is_set() and not self.stop:
                success, img = self.cap.read()

                if not success:
                    self.logger.log_error("Error reading camera data")
                    continue

                processedImage = self._preprocessImage(img)
                self._processFrame(processedImage)

                #cv2.imshow("img", processedImage)

                #if cv2.waitKey(1) & 0xFF == 27:
                #    break

        except Exception as e:
            self.logger.log_error("Something went wrong. {}".format(str(e)))

        self.cap.release()
        cv2.destroyAllWindows()

    def release(self):
        self.stop = True

    def _preprocessImage(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        return blurred
    
    def _processFrame(self, img):
        barcodes = decode(img, [ZBarSymbol.QRCODE])

        for barcode in barcodes:
            code = barcode.data.decode('utf-8')
            now = time.time()

            # Avoid retriggering same code too fast
            if code == self.last_code and (now - self.last_time < self.QR_SCAN_COOLDOWN):
                continue

            self.last_code, self.last_time = code, now
            self.logger.log_info(f"Detected QR: {code}")
            self.queue.put(code)
