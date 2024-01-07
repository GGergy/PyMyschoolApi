from abc import ABC, abstractmethod


safemode = False


class Model(ABC):
    _url = ""
    _raw = ""
    _exception = False

    @abstractmethod
    def parse_json_response(self, response):
        """parse api response"""

    @abstractmethod
    def request_url(self):
        """build request url"""

    @property
    def raw_data(self):
        return self._raw

    @property
    def api_exception(self):
        return self._exception


class CollectionUnion(ABC):

    def __init__(self, data):
        self._collection = self._parse_data(data)

    @abstractmethod
    def _parse_data(self, data):
        pass

    def __len__(self):
        return len(self._collection)

    @abstractmethod
    def __getitem__(self, item):
        pass

    def __str__(self):
        return str(self._collection)


class InvalidOrExpiredTokenError(Exception):
    def __str__(self):
        return "Your token is invalid or experied. Try to get a new one"


class EthernalApiError(Exception):
    def __str__(self):
        return "Response status code is not 200. Please try again later"


class WrapperError(Exception):
    def __str__(self):
        return (f"Wrapper is crashed, sorry. You can post an issue to my github:\n"
                f"https://github.com/GGergy/PyMyschoolApi/issues")
