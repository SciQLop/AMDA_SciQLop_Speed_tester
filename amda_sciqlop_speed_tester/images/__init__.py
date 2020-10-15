import pkg_resources
from amda_sciqlop_speed_tester.speed_teser_sequence import SEQUENCE_HTML, ITEMS
import pathlib

_DONE_ = "&#10004;"
_PENDING_ = "&#10144;"
#_PENDING_ = '<div class="loader"></div>'

_ITEMS = list(ITEMS) + ["result"]


def _clear_status():
    return {item: "" for item in _ITEMS}


class MainPage:
    def __init__(self):
        self._content = open(pkg_resources.resource_filename('amda_sciqlop_speed_tester.images',
                                                             'page.html'), 'r').read()
        self._status = _clear_status()

    @staticmethod
    def _get_status(value):
        if value == "done":
            return _DONE_
        if value == "pending":
            return _PENDING_
        return value

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in _ITEMS:
                self._status[key] = self._get_status(value)

    def html(self):
        return self._content.format(sequence=SEQUENCE_HTML.format(**self._status),
                                    result=self._status['result'])
