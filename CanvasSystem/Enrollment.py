from CanvasSystem.AbstractCanvasObject import AbstractCanvasObject


class Enrollment(AbstractCanvasObject):
    def __init__(self, obj, course_id=None, term_id=None, in_as='json'):
        if in_as == 'json':
            self._student_id = obj['id']
            self._course_id = course_id
            self._term_id = term_id
        elif in_as == 'csv':
            self._term_id, self._course_id, self._student_id = obj.split(',')
        else:
            raise TypeError("in_as needs to be a string in ['json', 'csv'] or not passed and default to json")

    def as_csv_line(self):
        # term_id,course_id,student_id
        return f'{self._term_id},{self._course_id},{self._student_id}\n'

    @property
    def student_id(self):
        return self._student_id

    @property
    def course_id(self):
        return self._course_id

    @property
    def term_id(self):
        return self._term_id

    def __str__(self): return f'{self._term_id},{self._course_id},{self._student_id.strip()}'

    def __repr__(self): return f'{self._term_id},{self._course_id},{self._student_id.strip()}'
