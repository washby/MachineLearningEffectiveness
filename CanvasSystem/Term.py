from CanvasSystem.AbstractCanvasObject import AbstractCanvasObject


class Term(AbstractCanvasObject):
    def __init__(self, obj, in_as="json"):
        if obj is None:
            raise ValueError
        if in_as == "json":
            self._json = obj
            self._name = obj['name']
            self._id = obj['id']
            self._active = True if obj['workflow_state'] == 'active' else False
            start_at_string = obj['start_at']
            end_at_string = obj['end_at']
            self._set_start_end_dates(start_at_string, end_at_string)
        elif in_as == "csv":
            self._json = None
            self._id, self._name, start_at_string, end_at_string, active = obj.split(',')
            self._set_start_end_dates(start_at_string, end_at_string)
            self._active = active == "True"

    def is_active(self):
        return self._active

    def as_json(self):
        return self._json

    def as_csv_line(self):
        # ID,Name,Start Date,End Date,Active
        return f'{self._id},{self._name},{self._start_date},{self._end_date},{self._active}\n'

    def __str__(self):
        return f"{self._name}({self._id})->Starts:{self._start_date};Ends:{self._end_date}"

    def __repr__(self):
        return str(self._json)

    def __eq__(self, other):
        if type(other) != Term:
            raise TypeError(f"Cannot compare Term to {type(other)}")
        return self.__json == other.as_json()

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if type(other) != Term:
            raise TypeError(f"Cannot compare Term to {type(other)}")
        if self._start_date is None:
            return True
        if other.start_date is None:
            return False
        return self._start_date > other.start_date

    def __ge__(self, other):
        if type(other) != Term:
            raise TypeError(f"Cannot compare Term to {type(other)}")
        if self._start_date is None:
            return True
        if other.start_date is None:
            return False
        return self._start_date >= other.start_date

    def __le__(self, other):
        if type(other) != Term:
            raise TypeError(f"Cannot compare Term to {type(other)}")
        if self._start_date is None:
            return False
        if other.start_date is None:
            return True
        return self._start_date <= other.start_date

    def __lt__(self, other):
        if type(other) != Term:
            raise TypeError(f"Cannot compare Term to {type(other)}")
        if self._start_date is None:
            return False
        if other.start_date is None:
            return True
        return self._start_date < other.start_date
