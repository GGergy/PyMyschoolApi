from .model import Model, convert_date
from requests import Session


class Schedule(Model):
    _base = 'https://authedu.mosreg.ru/api/family/web/v1'

    def __init__(self, auth_token, student_id, date):
        self.summary = str
        self.date = str
        self.activities = list
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
        self.activities = [Lesson(item) for item in response['activities'] if item['type'] == 'LESSON']


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
        self.marks = [Mark(item) for item in data['lesson']['marks']]


class Teacher:
    def __init__(self, data: dict):
        for key, item in data.items():
            self.__setattr__(key, item)


class Mark:
    def __init__(self, data):
        self.id = data['id']
        self.value = data['value']
        self.comment = data['comment']
        self.control_form_name = data['control_form_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
