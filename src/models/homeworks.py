from .model import Model, safemode, convert_date
from requests import Session


class Homework:
    def __init__(self, response):
        self.description = response['description']
        self.comments = response['comments']
        self.attachments = AttachmentUnion(response['additional_materials'])
        self.date = response['date']
        self.subject_id = response['subject_id']
        self.subject_name = response['subject_name']

    def __repr__(self):
        return f'"{self.description}, date - {self.date}, subject - {self.subject_name}"'


class Homeworks(Model):
    _base = 'https://authedu.mosreg.ru/api/family/web/v1'

    def __init__(self, auth_token, student_id, date_from, date_to):
        self._homeworks = []
        self._session = Session()
        if safemode:
            try:
                self._parse_json_response(self._request(auth_token, student_id, date_from, date_to))
            except Exception as e:
                self._exception = repr(e)
        else:
            self._parse_json_response(self._request(auth_token, student_id, date_from, date_to))

    def _request(self, auth_token, student_id, date_from, date_to):
        response = self._session.get(url=f'{self._base}/homeworks',
                                     headers={"Auth-Token": auth_token, "X-mes-subsystem": "familyweb"},
                                     params={'student_id': str(student_id), 'from': convert_date(date_from),
                                             'to': convert_date(date_to)})
        self._url = response.url
        self._raw = response.text
        return response.json()

    def _parse_json_response(self, response: dict):
        self._homeworks = [Homework(data) for data in response['payload']]

    def __getitem__(self, item) -> Homework:
        return self._homeworks[item]

    def __len__(self):
        return len(self._homeworks)

    def __str__(self):
        return str(self._homeworks)


class FileAttachment:
    def __init__(self, data):
        self.type = 'file'
        self.title = data['title']
        self.size = data['file_size']
        self.link = data['link']
        self.description = data['description']

    def __repr__(self):
        return self.title


class BookAttachment:
    def __init__(self, data):
        self.type = 'book'
        self.title = data['title']
        self.description = data['description']
        self.urls = data['urls']

    def __repr__(self):
        return self.title


class AttachmentUnion:
    def __init__(self, data):
        self._attachments = [FileAttachment(i) if item['type'] == 'attachments' else BookAttachment(i)
                             for item in data for i in item['items']]

    def __getitem__(self, item) -> BookAttachment | FileAttachment:
        return self._attachments[item]

    def __len__(self):
        return len(self._attachments)

    def __str__(self):
        return str(self._attachments)
