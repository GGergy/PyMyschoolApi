import datetime

import requests

from .models.model import EthernalApiError, InvalidOrExpiredTokenError, WrapperError, safemode
from .models.homeworks import Homeworks
from .models.profile import Profile
from .models.schedule import Schedule
from .models.week_shedule import WeekSchedule
from .token_util import get_new_token


class MyschoolClient:
    def __init__(self, auth_token: str):
        self._token = auth_token
        self._session = requests.Session()
        self._profile = self._request(Profile())

    @property
    def profile(self) -> Profile:
        return self._profile

    def get_schedule(self, date: datetime.date) -> Schedule:
        return self._request(Schedule(student_id=self.profile.id, date=date))

    def get_homework(self, date_from: datetime.date, date_to: datetime.date) -> Homeworks:
        return self._request(
            Homeworks(
                student_id=self.profile.id,
                date_from=date_from,
                date_to=date_to,
            ),
        )

    def get_shedules_by_dates(self, dates: list[datetime.date]) -> WeekSchedule:
        return self._request(WeekSchedule(student_id=self.profile.id, dates=dates))

    def _request(self, model):
        try:
            self._send_request(model)
        except InvalidOrExpiredTokenError:
            if not safemode:
                ans = input("Invalid token. Do you want to get new one? (Y/n) ")
                if ans.lower() == "y":
                    new_token = get_new_token()
                    if new_token:
                        self._token = new_token
                        print("Success!")
                        return self._request(model)
                    else:
                        print("Cannot get new token")
                raise InvalidOrExpiredTokenError()
            print(str(InvalidOrExpiredTokenError()))
        except EthernalApiError:
            if not safemode:
                raise EthernalApiError()
            print(str(EthernalApiError()))
        except Exception as e:
            if not safemode:
                raise WrapperError()
            model._exception = repr(e)
            print(str(WrapperError()))
        return model

    def _send_request(self, model):
        url = model.request_url()
        response = self._session.get(url=url, headers={"Auth-Token": self._token, "X-mes-subsystem": "familyweb"})
        if response.status_code == 401:
            raise InvalidOrExpiredTokenError()
        if response.status_code != 200:
            raise EthernalApiError()
        model.parse_json_response(response.json())
