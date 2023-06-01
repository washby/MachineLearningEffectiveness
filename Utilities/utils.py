import base64
import re
from datetime import datetime

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_course_info(course_json_object):
    course_level = -1
    course_credit_count = -1
    try:
        crs = course_json_object['course_code']
        pattern = r'[a-zA-Z\-]{2,4}(\d)\d{3}'
        matches = re.findall(pattern, crs)
        matches = list(set(matches))
        if len(matches) == 0:
            course_level = -1
        elif len(matches) == 1:
            course_level = int(matches[0])
        else:
            course_level = min([int(x) for x in matches])

        pattern = r'[a-zA-Z\-]{2,4}\d(\d)\d{2}'
        matches = re.findall(pattern, crs)
        matches = list(set(matches))
        if len(matches) == 0:
            course_credit_count = -1
        elif len(matches) == 1:
            course_credit_count = int(matches[0])
        course_credit_count = min([int(x) for x in matches])
        if course_credit_count == 0:
            course_credit_count = 3
    except KeyError:
        pass
    return course_level, course_credit_count

def get_week_of_year(date):
    return date.isocalendar()[1]