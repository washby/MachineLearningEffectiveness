from CanvasSystem.AbstractCanvasObject import AbstractCanvasObject


class Course(AbstractCanvasObject):
    def __init__(self, obj, in_as='json'):
        if obj is None:
            raise ValueError
        if in_as == 'json':
            self._start_date = None
            self._end_date = None
            self._id = obj['id']
            self._integration_id = obj['integration_id']
            self._sis_course_id = obj['sis_course_id']
            self._name = obj['name'].replace(',', '_')
            self._enrollment_term_id = obj['enrollment_term_id']
            start_at_string = obj['start_at']
            end_at_string = obj['end_at']
            self._set_start_end_dates(start_at_string, end_at_string)
        elif in_as == 'csv':
            self._start_date = None
            self._end_date = None
            self._json = None
            # print(f'reading in csv line {obj}')
            self._enrollment_term_id, self._id, self._name, start_at_string, end_at_string = obj.split(',')
            self._set_start_end_dates(start_at_string, end_at_string)
        else:
            raise ValueError("in_as must by in ['json', csv'] or empty which defaults to json")

    def as_csv_line(self):
        return f'{self._enrollment_term_id},{self._id},{self._name},{self._start_date},{self._end_date}\n'

    @property
    def term_id(self):
        return self._enrollment_term_id

    def __str__(self):
        return self.as_csv_line()

    def __repr__(self):
        return self.as_csv_line()
