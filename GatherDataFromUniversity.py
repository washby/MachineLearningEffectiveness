import Utilities.GatherFunctions as gf
from CanvasSystem.CanvasConnection import CanvasSystem
from Utilities.Encryption import Encryption
from Utilities.GatherFunctions import gather_enrollments
from Utilities.Settings import Settings
import pandas as pd
import numpy as np
# PULL_FROM_SERVER is a flag for testing and will be set to True when run
# for the research study. Since data will be pulled and stored locally
# the flag allows for faster build time by not repeatedly having to pull
# from the server while being built.
# PULL_FROM_SERVER = False
# PULL_TERMS_FROM_SERVER = True
# PULL_COURSES_FROM_SERVER = True
# PULL_ENROLLMENTS_FROM_SERVER = True
# ENCYRPT_DATA = False

settings = Settings(pull_override=False, pull_terms=True, pull_courses=True, pull_enrollments=True, encrypt=False)

# List of the file names that will be used to store data locally
TERMS_FILE = 'canvas_terms.csv'
COURSES_FILE = 'canvas_courses.csv'
ENROLLMENT_FILE = 'canvas_enrollments.csv'
STUDENT_RECORD_FILE = 'student_per_term.csv'

# Create CanvasSystem object to make API calls based on config file passed
canvas = CanvasSystem('Test.json')

encryption_obj = None
if settings.ENCYRPT_DATA:
    salt = canvas.get_salt()
    print("This password is unique to this run and will not be saved anywhere. Therefore to decrypt the ", end='')
    print("information you will need to be able to reenter the password so ensure it is known or recorded.")
    pw = input("Create Password: ")
    encryption_obj = Encryption(salt, pw)
###################################################################
###    Gather all the enrollment terms from the Canvas system   ###
###################################################################
terms = gf.gather_emrollment_terms(settings, canvas, TERMS_FILE, encryption_obj)

###################################################################
###    Gather all the courses in the needed terms from Canvas   ###
###################################################################
courses, crs_dict = gf.gather_courses(settings, canvas, terms, COURSES_FILE, encryption_obj)

###################################################################
###    Gather all the enrollments in the courses from Canvas    ###
###################################################################
enrollments = gf.gather_enrollments(settings, canvas, courses, ENROLLMENT_FILE, encryption_obj)
term_ids = []
course_ids = []
student_ids = []
crs_level = []
crs_credits = []
for enrl in enrollments:
    term_ids.append(enrl.term_id)
    course_ids.append(enrl.course_id)
    student_ids.append(enrl.student_id)
    crs_level.append(crs_dict[enrl.course_id].course_level)
    crs_credits.append(crs_dict[enrl.course_id].course_credit_count)
student_per_term_df = pd.DataFrame({'term_id': term_ids, 'course_id': course_ids, 'student_id': student_ids,
                               'course_level': crs_level, 'course_credits': crs_credits})
student_per_term_df['course_count'] = student_per_term_df.groupby(['student_id', 'term_id'])['course_id'].transform('count')
student_per_term_df['course_level_avg'] = student_per_term_df.groupby(['student_id', 'term_id'])['course_level'].transform('mean')
student_per_term_df['course_credit_sum'] = student_per_term_df.groupby(['student_id', 'term_id'])['course_credits'].transform('sum')
student_per_term_df.drop(['course_level', 'course_credits'], axis=1, inplace=True)

student_per_term_df.to_csv(STUDENT_RECORD_FILE, index=False)

# TODO: Calculate average submission date per user per term
for index, record in student_per_term_df.head(1).iterrows():
    print(record)
    result = canvas.get_course_assignments_info(record['course_id'], record['student_id'])
    for item in result:
        print(item)
        for k,v in item.items():
            print(f'{k}->: {v}')
        print('\n------\n')

# TODO: Get final grade in course per user per term

# TODO: Query message activity per user per term

# TODO: Query discussion board activity per course per user per term

# TODO: Calculate weekly login average per user per term

