import requests
from fit_manage_qr_detector.logger import Logger

class Validator:
    BASE_SERVER_URL = 'https://www.fitmanageapp.com/api/access/validate/{}'
    SUCCESS_CODE = 200
    RESPONSE_TIMEOUT_IN_S = 3

    def __init__(self, logger: Logger):
        self.logger = logger

    def validate(self, code: str) -> bool:
        try:
            response = requests.get(self.BASE_SERVER_URL.format(code), timeout=self.RESPONSE_TIMEOUT_IN_S)
            return response.status_code == self.SUCCESS_CODE
        except requests.RequestException as e:
            self.logger.log_error("Request failed: {}".format(e))
            return False

