import datetime
import traceback
from json import JSONDecodeError
from typing import List

import requests

from .models.model import EthernalApiError, InvalidOrExpiredTokenError, WrapperError
from .models.homeworks import Homeworks
from .models.profile import Profile
from .models.schedule import Schedule
from .models.week_shedule import WeekSchedule
from .token_util import get_new_token


# Клиент, через который идут запросы
class MyschoolClient:
    def __init__(self, auth_token: str, interactive: bool = True):
        self.interactive = interactive  # Будет ли получать новый токен через selenium (модуль token_util)
        self._token = auth_token
        self._session = requests.Session()
        self._profile = self._request(Profile())

    @property
    def profile(self) -> Profile:
        """Профиль пользователя в Моей Школе"""
        return self._profile

    def get_schedule(self, date: datetime.date) -> Schedule:
        """Расписание одного дня. Date - тот самый день"""
        return self._request(Schedule(student_id=self.profile.id, date=date))

    def get_homework(self, date_from: datetime.date, date_to: datetime.date) -> Homeworks:
        """Домашняя работа на период дней (верхняя граница не включительна)"""
        return self._request(
            Homeworks(
                student_id=self.profile.id,
                date_from=date_from,
                date_to=date_to,
            ),
        )

    def get_shedules_by_dates(self, dates: List[datetime.date]) -> WeekSchedule:
        """Расписание"""
        return self._request(WeekSchedule(student_id=self.profile.id, dates=dates))

    def _request(self, model):
        try:
            self._send_request(model)
        except InvalidOrExpiredTokenError:
            if self.interactive:
                if self._get_token_from_console():
                    return self._request(model)
            else:
                raise InvalidOrExpiredTokenError()
        except EthernalApiError:
            raise EthernalApiError()
        except Exception:
            new_exc = WrapperError(context=traceback.format_exc())
            model._exception = new_exc
            raise new_exc
        return model

    def _send_request(self, model):
        url = model.request_url()
        response = self._session.get(url=url, headers={"Auth-Token": self._token, "X-mes-subsystem": "familyweb"})
        if response.status_code == 401:
            model._exception = InvalidOrExpiredTokenError
            raise InvalidOrExpiredTokenError()
        try:
            response_json = response.json()
        except JSONDecodeError:
            response_json = None
        if response.status_code != 200 or not response_json:
            model._exception = EthernalApiError
            raise EthernalApiError()
        model.parse_json_response(response_json)

    def set_token(self, new_token: str):
        """Задать новый токен"""
        self._token = new_token

    def _get_token_from_console(self):
        ans = input("Invalid token. Do you want to get a new one? (Y/n) ")
        if ans.lower() == "y":
            new_token = get_new_token()
            if new_token:
                self._token = new_token
                print("Success!")
                return True
            else:
                print("Cannot get new token")
        else:
            raise InvalidOrExpiredTokenError()

    def check_token(self) -> bool:
        """Проверить токен на валидность"""
        try:
            self._request(Profile())
            return True
        except InvalidOrExpiredTokenError:
            return False
