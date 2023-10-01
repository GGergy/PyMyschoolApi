from .model import Model, safemode
from requests import Session


class Profile(Model):
    _base = 'https://authedu.mosreg.ru/api/family/web/v1'

    def __init__(self, auth_token):
        self.last_name = str
        self.middle_name = str
        self.first_name = str
        self.birth_date = str
        self.sex = str
        self.user_id = int
        self.id = int
        self.phone = str
        self.email = str
        self.contract_id = str
        self.snils = str
        self.type = str
        self._session = Session()
        if safemode:
            try:
                self._parse_json_response(self._request(auth_token))
            except Exception as e:
                self._exception = repr(e)
        else:
            self._parse_json_response(self._request(auth_token))

    def _request(self, auth_token):
        response = self._session.get(url=f'{self._base}/profile',
                                     headers={"Auth-Token": auth_token, "X-mes-subsystem": "familyweb"})
        self._url = response.url
        self._raw = response.text
        return response.json()

    def _parse_json_response(self, response: dict):
        for key, item in response['profile'].items():
            self.__setattr__(key, item)

    def __str__(self):
        return (f'{self.last_name} {self.first_name} {self.middle_name}: type - {self.type}, student_id - {self.id},'
                f' phone number - 8{self.phone}, email - {self.email}.')
