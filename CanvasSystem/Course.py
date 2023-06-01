from CanvasSystem.AbstractCanvasObjectWithDates import AbstractCanvasObjectWithDates
from Utilities.utils import get_course_info

class Course(AbstractCanvasObjectWithDates):
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
            self._course_level, self._course_credit_count = get_course_info(obj)
            start_at_string = obj['start_at']
            end_at_string = obj['end_at']
            self._set_start_end_dates(start_at_string, end_at_string)
            self._course_code = obj['course_code']
        elif in_as == 'csv':
            self._start_date = None
            self._end_date = None
            self._json = None
            self._enrollment_term_id, self._id, self._name, self._course_level, self._course_credit_count, start_at_string, end_at_string = obj.split(',')
            self._course_credit_count = int(self._course_credit_count)
            self._course_level = int(self._course_level)
            self._set_start_end_dates(start_at_string, end_at_string)
        else:
            raise ValueError("in_as must by in ['json', csv'] or empty which defaults to json")

    def as_csv_line(self):
        return f'{self._enrollment_term_id},{self._id},{self._name},{self._course_level},{self._course_credit_count},{self._start_date},{self._end_date}\n'

    def encrypt(self, encryption_obj):
        self._id = encryption_obj.encrypt(str(self._id))
        self._enrollment_term_id = encryption_obj.encrypt(str(self._enrollment_term_id))
        self._name = encryption_obj.encrypt(self._name)

    def decrypt(self, encryption_obj):
        self._id = encryption_obj.decrypt(self._id)
        self._name = encryption_obj.decrypt(self._name)
        self._enrollment_term_id = encryption_obj.decrypt(self._enrollment_term_id)

    @property
    def course_level(self): return self._course_level
    @property
    def term_id(self): return self._enrollment_term_id

    @property
    def course_credit_count(self): return self._course_credit_count

    def __str__(self): return self.as_csv_line()

    def __repr__(self): return self.as_csv_line()
