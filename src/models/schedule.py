from .model import Model, convert_date
from requests import Session


class Schedule(Model):
    _base = 'https://authedu.mosreg.ru/api/family/web/v1'

    def __init__(self, auth_token, student_id, date):
        self.summary = str
        self.date = str
        self.activities = LessonUnion
        self.has_homework = bool
        self._session = Session()
        try:
            self._parse_json_response(self._request(auth_token, student_id, date))
        except Exception as e:
            self._exception = repr(e)

    def _request(self, auth_token, student_id, date):
        response = self._session.get(url=f'{self._base}/schedule',
                                     headers={"Auth-Token": auth_token, "X-mes-subsystem": "familyweb"},
                                     params={'student_id': str(student_id), 'date': convert_date(date)})
        self._url = response.url
        self._raw = response.text
        return response.json()

    def _parse_json_response(self, response: dict):
        self.summary = response['summary']
        self.date = response['date']
        self.has_homework = response['has_homework']
        self.activities = LessonUnion(response['activities'])

    def __str__(self):
        return f'Summary - {self.summary}, date - {self.date}'


class Lesson:
    def __init__(self, data: dict):
        self.info = data['info']
        self.begin_time = data['begin_time']
        self.end_time = data['end_time']
        self.room_number = data['room_number']
        self.room_name = data['room_name']
        self.building_name = data['building_name']
        self.subject_id = data['lesson']['subject_id']
        self.subject_name = data['lesson']['subject_name']
        self.homework = data['lesson']['homework']
        self.teacher = Teacher(data['lesson']['teacher'])
        self.marks = MarkUnion(data['lesson']['marks'])

    def __repr__(self):
        return (f'"{self.info}. begin time - {self.begin_time}. end time - {self.end_time}. teacher - {self.teacher}.'
                f' room number - {self.room_number}"')


class LessonUnion:
    def __init__(self, data):
        self._lessons = [Lesson(item) for item in data if item['type'] == 'LESSON']

    def lesson_at(self, index: int) -> Lesson:
        return self.__getitem__(index)

    def __getitem__(self, item):
        return self._lessons[item]

    def __len__(self):
        return len(self._lessons)

    def __str__(self):
        return str(self._lessons)


class Teacher:
    def __init__(self, data: dict):
        self.last_name = str
        self.middle_name = str
        self.first_name = str
        self.birth_date = str
        self.sex = str
        self.user_id = int
        for key, item in data.items():
            self.__setattr__(key, item)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Mark:
    def __init__(self, data):
        self.id = data['id']
        self.value = data['value']
        self.comment = data['comment']
        self.control_form_name = data['control_form_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __repr__(self):
        return f'"value - {self.value}, created at {self.created_at}, control from - {self.control_form_name}"'


class MarkUnion:
    def __init__(self, data):
        self._marks = [Mark(item) for item in data]

    def mark_at(self, index: int) -> Mark:
        return self.__getitem__(index)

    def __getitem__(self, item):
        return self._marks[item]

    def __len__(self):
        return len(self._marks)

    def __str__(self):
        str(self._marks)
