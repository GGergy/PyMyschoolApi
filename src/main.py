import datetime
from .models.profile import Profile
from .models.schedule import Schedule
from .models.homeworks import Homeworks


class MyschoolClient:
    def __init__(self, auth_token: str):
        self.__token = auth_token
        self.profile = Profile(auth_token=auth_token)

    def get_schedule(self, date: datetime.date):
        return Schedule(self.__token, student_id=self.profile.id, date=date)

    def get_homework(self, date_from: datetime.date, date_to: datetime.date):
        return Homeworks(self.__token, student_id=self.profile.id, date_from=date_from, date_to=date_to)
