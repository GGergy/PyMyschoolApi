from .model import Model


class Profile(Model):
    _base = "https://authedu.mosreg.ru/api/family/web/v1"

    def __init__(self):
        self.last_name = ""
        self.middle_name = ""
        self.first_name = ""
        self.birth_date = ""
        self.sex = ""
        self.user_id = 0
        self.id = 0
        self.phone = ""
        self.email = ""
        self.contract_id = ""
        self.snils = ""
        self.type = ""

    def request_url(self):
        if not self._url:
            self._url = f"{self._base}/profile"
        return self._url

    def parse_json_response(self, response: dict):
        for key, item in response["profile"].items():
            self.__setattr__(key, item)
        self._raw = response

    def __str__(self):
        return (
            f"{self.last_name} {self.first_name} {self.middle_name}: type - {self.type}, student_id - {self.id},"
            f" phone number - 8{self.phone}, email - {self.email}"
        )
