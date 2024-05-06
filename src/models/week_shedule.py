import datetime
from typing import List

from .model import Model, CollectionUnion


class ScheduleDay:
    def __init__(self, data):
        self.date = data["date"]
        self.lessons = LessonUnion(data["lessons"])

    def __repr__(self):
        return f'"date - {self.date}, lessons - {len(self.lessons)}"'


class WeekSchedule(Model):
    _base = "https://authedu.mosreg.ru/api/family/web/v1"

    def __init__(self, student_id, dates: List[datetime.date]):
        self._student_id = student_id
        self._dates = dates
        self._days = List[ScheduleDay]

    def request_url(self):
        if not self._url:
            self._url = (
                f"{self._base}/schedule/short?"
                f"dates={'%2C'.join(map(str, self._dates))}&student_id={self._student_id}"
            )
        return self._url

    def parse_json_response(self, response):
        self._days = [ScheduleDay(data) for data in response["payload"]]
        self._raw = response

    def __getitem__(self, item) -> ScheduleDay:
        return self._days[item]

    def __len__(self):
        return len(self._days)

    def __str__(self):
        return str(self._days)


class Lesson:
    def __init__(self, data: dict):
        self.id = data["lesson_id"]
        self.name = data["lesson_name"]
        self.begin_time = data["begin_time"]
        self.end_time = data["end_time"]
        self.subject_id = data["subject_id"]
        self.subject_name = data["subject_name"]
        self.is_virtual = data["is_virtual"]
        self.group_name = data["group_name"]
        self.lesson_type = data["lesson_type"]

    def __repr__(self):
        return f"{self.group_name}. begin time - {self.begin_time}. end time - {self.end_time}"


class LessonUnion(CollectionUnion):
    def _parse_data(self, data):
        return [Lesson(item) for item in data]

    def __getitem__(self, item) -> Lesson:
        return self._collection[item]
