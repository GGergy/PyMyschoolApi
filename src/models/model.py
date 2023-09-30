import datetime
from abc import ABC, abstractmethod


safemode = True


class Model(ABC):
    _url = 'api request url'
    _raw = 'api raw response'
    _exception = False

    @abstractmethod
    def _request(self, **kwargs):
        """make request to api"""

    @abstractmethod
    def _parse_json_response(self, response):
        """parse api response"""

    @property
    def raw_data(self):
        return self._raw

    @property
    def request_url(self):
        return self._url

    @property
    def api_exception(self):
        return self._exception


def convert_date(date: datetime.date):
    return date.strftime('%Y-%m-%d')
