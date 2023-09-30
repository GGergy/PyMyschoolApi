from .models.profile import Profile
from .models.schedule import Schedule


class MyschoolClient:
    def __init__(self, auth_token):
        self.__token = auth_token
        self.profile = Profile(auth_token=auth_token)

    def get_schedule(self, date):
        return Schedule(self.__token, student_id=self.profile.id, date=date)
