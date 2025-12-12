import requests
from fit_manage_qr_detector.logger import Logger

class Validator:
    GYM_ID = '64b2ce75722116cbbfa55501' # ToDo: Get this values dynamically

    BASE_SERVER_URL = 'https://www.fitmanageapp.com/api/access/validate/{}' + GYM_ID
    SUCCESS_CODE = 200
    RESPONSE_TIMEOUT_IN_S = 3
    SECRET = 'a92e6bc9294990d8a6f3eace74c41eaaa4bcc7a858b06f40649ed98f90afe1c4'

    def __init__(self, logger: Logger):
        self.logger = logger

    def validate(self, code: str) -> bool:
        try:
            url = self.BASE_SERVER_URL.format(code)
            headers = { 'Authorization': self.SECRET }
            response = requests.get(url, headers=headers, timeout=self.RESPONSE_TIMEOUT_IN_S)
            return response.status_code == self.SUCCESS_CODE
        except requests.RequestException as e:
            self.logger.log_error("Request failed: {}".format(e))
            return False

