from datetime import datetime, timezone

from CanvasSystem.CanvasConnection import CanvasSystem
from CanvasSystem.Course import Course
from CanvasSystem.Enrollment import Enrollment
from CanvasSystem.Term import Term

# PULL_FROM_SERVER is a flag for testing and will be set to True when run
# for the research study. Since data will be pulled and stored locally
# the flag allows for faster build time by not repeatedly having to pull
# from the server while being built.
PULL_FROM_SERVER = False
PULL_TERMS_FROM_SERVER = True
PULL_COURSES_FROM_SERVER = False
PULL_ENROLLMENTS_FROM_SERVER = False

# List of the file names that will be used to store data locally
TERMS_FILE = 'terms.csv'
COURSES_FILE = 'courses.csv'
ENROLLMENT_FILE = 'enrollments.csv'

# Create CanvasSystem object to make API calls based on config file passed
canvas = CanvasSystem('Test.json')
salt = canvas.get_salt()
print("This password is unique to this run and will not be saved anywhere. Therefore to decrypt the ", end='')
print("information you will need to be able to reenter the password so ensure it is known or recorded.")
pw = input("Create Password: ")
###################################################################
###    Gather all the enrollment terms from the Canvas system   ###
###################################################################
if PULL_FROM_SERVER and PULL_TERMS_FROM_SERVER:
    terms = canvas.get_all_terms()
    # remove any duplicates that got into the system
    term_dict = {}
    for term in terms:
        term_dict[term.id] = term
    terms = [v for k, v in term_dict.items()]
    terms.sort()
    with open(TERMS_FILE, 'wb') as file:
        file.write('id,name,start_date,end_date,is_available\n')
        for term in terms:
            if term.start_date is not None and term.start_date <= datetime.now(tz=timezone.utc) \
                    and term.end_date <= datetime.now(tz=timezone.utc):
                term.encrypt(salt, pw)
                file.write(term.as_csv_line())
else:
    lines = None
    terms = []
    with open(TERMS_FILE) as file:
        lines = file.readlines()
        for line in lines[1:]:
            term = Term(line, in_as='csv')
            term.decrypt(salt, pw)
            terms.append(term)


###################################################################
###    Gather all the courses in the needed terms from Canvas   ###
###################################################################
courses = []
if PULL_FROM_SERVER and PULL_COURSES_FROM_SERVER:
    courses = canvas.get_all_courses_in_terms(terms)
    with open(COURSES_FILE, 'w') as file:
        file.write('term_id,id,name,course_level,start_date,end_date\n')
        for course in courses:
            file.write(course.as_csv_line())
else:
    with open(COURSES_FILE) as file:
        lines = file.readlines()[1:]
        for line in lines:
            courses.append(Course(line, in_as='csv'))


###################################################################
###    Gather all the enrollments in the courses from Canvas    ###
###################################################################
enrollments = []
if PULL_FROM_SERVER and PULL_ENROLLMENTS_FROM_SERVER:
    enrollments = canvas.get_all_course_enrollments(courses)
    with open(ENROLLMENT_FILE, 'w') as file:
        file.write('term_id,course_id,student_id\n')
        for enrollment in enrollments:
            file.write(enrollment.as_csv_line())
else:
    with open(ENROLLMENT_FILE) as file:
        lines = file.readlines()[1:]
        for line in lines:
            enrollments.append(Enrollment(line, in_as='csv'))

###################################################################
###    Build Student Information Setup    ###
###################################################################

print(terms)

