from .model import CollectionUnion, Model


class Homework:
    def __init__(self, response):
        self.description = response["description"]
        self.comments = response["comments"]
        self.attachments = AttachmentUnion(response["additional_materials"])
        self.date = response["date"]
        self.subject_id = response["subject_id"]
        self.subject_name = response["subject_name"]

    def __repr__(self):
        return f'"{self.description}, date - {self.date}, subject - {self.subject_name}"'


class Homeworks(Model):
    _base = "https://authedu.mosreg.ru/api/family/web/v1"

    def __init__(self, student_id, date_from, date_to):
        self._homeworks = []
        self._student_id = student_id
        self._date_from = date_from
        self._date_to = date_to

    def request_url(self):
        if not self._url:
            self._url = (
                f"{self._base}/homeworks" f"?student_id={self._student_id}&from={self._date_from}&to={self._date_to}"
            )
        return self._url

    def parse_json_response(self, response: dict):
        self._homeworks = [Homework(data) for data in response["payload"]]
        self._raw = response

    def __getitem__(self, item) -> Homework:
        return self._homeworks[item]

    def __len__(self):
        return len(self._homeworks)

    def __str__(self):
        return str(self._homeworks)


class FileAttachment:
    def __init__(self, data):
        self.type = "file"
        self.title = data["title"]
        self.size = data["file_size"]
        self.link = data["link"]
        self.description = data["description"]

    def __repr__(self):
        return f"File {self.title}, link - {self.link}"


class BookAttachment:
    def __init__(self, data):
        self.type = "book"
        self.title = data["title"]
        self.description = data["description"]
        self.urls = data["urls"]

    def __repr__(self):
        return f"Book {self.title}"


class CDZAttachment:
    def __init__(self, data):
        self.type = "cdz"
        self.title = data["title"]
        self.description = data["description"]
        self.urls = data["urls"]
        self.id = data["id"]
        # Только для МЭШ
        self.link = f"https://uchebnik.mos.ru/exam/challenge/{self.id}"

    def __repr__(self):
        return f"CDZ {self.title}, link - {self.link}"


class AttachmentUnion(CollectionUnion):
    _attachment_types = {"attachments": FileAttachment, "book": BookAttachment, "test_spec_binding": CDZAttachment}
    _data_type = BookAttachment | FileAttachment | CDZAttachment

    def _parse_data(self, data):
        response = []
        for collection in data:
            a_type = self._attachment_types.get(collection["type"])
            if not a_type:
                response.extend(collection["items"])
                continue
            response.extend([a_type(item) for item in collection["items"]])
        return response

    def __getitem__(self, item) -> _data_type:
        return self._collection[item]
