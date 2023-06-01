from datetime import datetime, timezone

from CanvasSystem.CanvasConnection import CanvasSystem
from CanvasSystem.Course import Course
from CanvasSystem.Enrollment import Enrollment
from CanvasSystem.Term import Term
from Utilities.Encryption import Encryption

# PULL_FROM_SERVER is a flag for testing and will be set to True when run
# for the research study. Since data will be pulled and stored locally
# the flag allows for faster build time by not repeatedly having to pull
# from the server while being built.
PULL_FROM_SERVER = False
PULL_TERMS_FROM_SERVER = True
PULL_COURSES_FROM_SERVER = True
PULL_ENROLLMENTS_FROM_SERVER = True
ENCYRPT_DATA = False

# List of the file names that will be used to store data locally
TERMS_FILE = 'canvas_terms.csv'
COURSES_FILE = 'canvas_courses.csv'
ENROLLMENT_FILE = 'canvas_enrollments.csv'

# Create CanvasSystem object to make API calls based on config file passed
canvas = CanvasSystem('Test.json')

if ENCYRPT_DATA:
    salt = canvas.get_salt()
    print("This password is unique to this run and will not be saved anywhere. Therefore to decrypt the ", end='')
    print("information you will need to be able to reenter the password so ensure it is known or recorded.")
    pw = input("Create Password: ")
    encryption_obj = Encryption(salt, pw)
###################################################################
###    Gather all the enrollment terms from the Canvas system   ###
###################################################################
if PULL_FROM_SERVER and PULL_TERMS_FROM_SERVER:
    terms = canvas.get_all_terms()
    # remove any duplicates that got into the system
    term_dict = {}
    for term in terms:
        term_dict[term.id] = term
    terms = None
    terms = [v for k, v in term_dict.items() if not(v.start_date is None or v.end_date is None)]
    terms.sort()
    with open(TERMS_FILE, 'w') as file:
        file.write('id,name,start_date,end_date,is_available\n')
        for term in terms:
            if ENCYRPT_DATA:
                term.encrypt(encryption_obj)
            file.write(term.as_csv_line())
else:
    lines = None
    terms = []
    with open(TERMS_FILE) as file:
        lines = file.readlines()
        for line in lines[1:]:
            terms.append(Term(line, in_as='csv'))

min_date = None
max_date = None
for term in terms:
    if ENCYRPT_DATA:
        term.decrypt(encryption_obj)
    # if term.start_date or term.end_date > time.time()
    if min_date is None or term.start_date < min_date:
        min_date = term.start_date
    if max_date is None or term.end_date > max_date:
        max_date = term.end_date

term_dict = {}
for term in terms:
    term_dict[term.id] = term

###################################################################
###    Gather all the courses in the needed terms from Canvas   ###
###################################################################
courses = []
if PULL_FROM_SERVER and PULL_COURSES_FROM_SERVER:
    courses = canvas.get_all_courses_in_terms(terms)
    with open(COURSES_FILE, 'w') as file:
        file.write('term_id,id,name,course_level,credit_count,start_date,end_date\n')
        for course in courses:
            if ENCYRPT_DATA:
                course.encrypt(encryption_obj)
            file.write(course.as_csv_line())
else:
    with open(COURSES_FILE) as file:
        lines = file.readlines()[1:]
        for line in lines:
            courses.append(Course(line, in_as='csv'))

if ENCYRPT_DATA:
    for course in courses:
        course.decrypt(encryption_obj)

crs_dict = {}
for course in courses:
    if course.id not in crs_dict:
        crs_dict[course.id] = course

###################################################################
###    Gather all the enrollments in the courses from Canvas    ###
###################################################################
enrollments = []
if PULL_FROM_SERVER and PULL_ENROLLMENTS_FROM_SERVER:
    enrollments = canvas.get_all_course_enrollments(courses)
    with open(ENROLLMENT_FILE, 'w') as file:
        file.write('term_id,course_id,student_id\n')
        for enrollment in enrollments:
            if ENCYRPT_DATA:
                enrollment.encrypt(encryption_obj)
            file.write(enrollment.as_csv_line())
else:
    with open(ENROLLMENT_FILE) as file:
        lines = file.readlines()[1:]
        for line in lines:
            enrollments.append(Enrollment(line, in_as='csv'))

if ENCYRPT_DATA:
    for enrollment in enrollments:
        enrollment.decrypt(encryption_obj)

###################################################################
###    Build Student Information Setup                          ###
###################################################################
# TODO: Calculate number of courses/credits per user per term
#Calculate number of courses per user per term
courses_per_user_per_term = {}
for enrollment in enrollments:
    if enrollment.term_id not in courses_per_user_per_term:
        courses_per_user_per_term[enrollment.term_id] = {}
    if enrollment.student_id not in courses_per_user_per_term[enrollment.term_id]:
        courses_per_user_per_term[enrollment.term_id][enrollment.student_id] = {}
        courses_per_user_per_term[enrollment.term_id][enrollment.student_id]['courses'] = 0
        courses_per_user_per_term[enrollment.term_id][enrollment.student_id]['crs_level'] = 0
        courses_per_user_per_term[enrollment.term_id][enrollment.student_id]['crs_crd_cnt'] = 0
    courses_per_user_per_term[enrollment.term_id][enrollment.student_id]['courses'] += 1
    courses_per_user_per_term[enrollment.term_id][enrollment.student_id]['crs_level'] += crs_dict[enrollment.course_id].course_level
    courses_per_user_per_term[enrollment.term_id][enrollment.student_id]['crs_crd_cnt'] += crs_dict[enrollment.course_id].course_credit_count

for term_id in courses_per_user_per_term:
    for student_id in courses_per_user_per_term[term_id]:
        count = courses_per_user_per_term[term_id][student_id]['courses']
        print(f"Term: {term_id} Student: {student_id}")
        print(f"---Course count: {count}")
        print(f"---Course level: {courses_per_user_per_term[term_id][student_id]['crs_level']/count}")
        print(f"---Course credit avg: {courses_per_user_per_term[term_id][student_id]['crs_crd_cnt']}")

# TODO: Calculate average course level per user per term

# TODO: Query message activity per user per term

# TODO: Query discussion board activity per course per user per term

# TODO: Calculate weekly login average per user per term

# TODO: Calculate average submission date per user per term
