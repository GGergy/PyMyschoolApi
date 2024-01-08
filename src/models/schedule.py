from .model import CollectionUnion, Model


class Schedule(Model):
    _base = "https://authedu.mosreg.ru/api/family/web/v1"

    def __init__(self, student_id, date):
        self._student_id = student_id
        self._date = date
        self.summary = ""
        self.date = ""
        self.activities = LessonUnion([])
        self.has_homework = bool

    def request_url(self):
        if not self._url:
            self._url = f"{self._base}/schedule?student_id={self._student_id}&date={self._date}"
        return self._url

    def parse_json_response(self, response: dict):
        self.summary = response["summary"]
        self.date = response["date"]
        self.has_homework = response["has_homework"]
        self.activities = LessonUnion(response["activities"])
        self._raw = response

    def __str__(self):
        return f"Summary - {self.summary}, date - {self.date}"


class Lesson:
    def __init__(self, data: dict):
        self.info = data["info"]
        self.begin_time = data["begin_time"]
        self.end_time = data["end_time"]
        self.room_number = data["room_number"]
        self.room_name = data["room_name"]
        self.building_name = data["building_name"]
        self.subject_id = data["lesson"]["subject_id"]
        self.subject_name = data["lesson"]["subject_name"]
        self.homework = data["lesson"]["homework"]
        self.replaced = data["lesson"]["replaced"]
        self.teacher = Teacher(data["lesson"]["teacher"])
        self.marks = MarkUnion(data["lesson"]["marks"])

    def __repr__(self):
        return (
            f'"{self.info}. begin time - {self.begin_time}. end time - {self.end_time}. teacher - {self.teacher}.'
            f' room number - {self.room_number}"'
        )


class LessonUnion(CollectionUnion):
    def _parse_data(self, data):
        return [Lesson(item) for item in data if item["type"] == "LESSON"]

    def __getitem__(self, item) -> Lesson:
        return self._collection[item]


class Teacher:
    def __init__(self, data: dict):
        self.last_name = ""
        self.middle_name = ""
        self.first_name = ""
        self.birth_date = ""
        self.sex = ""
        self.user_id = 0
        for key, item in data.items():
            self.__setattr__(key, item)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class Mark:
    def __init__(self, data):
        self.id = data["id"]
        self.value = data["value"]
        self.comment = data["comment"]
        self.control_form_name = data["control_form_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    def __repr__(self):
        return f'"value - {self.value}, created at {self.created_at}, control from - {self.control_form_name}"'


class MarkUnion(CollectionUnion):
    def _parse_data(self, data):
        return [Mark(item) for item in data]

    def __getitem__(self, item) -> Mark:
        return self._collection[item]
