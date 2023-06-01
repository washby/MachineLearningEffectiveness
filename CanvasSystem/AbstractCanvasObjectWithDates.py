from datetime import datetime


class AbstractCanvasObjectWithDates:
    def __init__(self):
        self._id = None
        self._end_date = None
        self._start_date = None
        self._name = None

    def _set_start_end_dates(self, start_at_string, end_at_string):
        if start_at_string is not None and start_at_string.strip() != 'None':
            self._start_date = datetime.fromisoformat(start_at_string.strip())
        if end_at_string is not None and end_at_string.strip() != 'None':
            self._end_date = datetime.fromisoformat(end_at_string.strip())

    @property
    def id(self):
        return self._id

    @property
    def end_date(self):
        return self._end_date

    @property
    def start_date(self):
        return self._start_date

    @property
    def name(self):
        return self._name
