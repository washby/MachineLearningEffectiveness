from CanvasSystem.Course import Course
from CanvasSystem.Enrollment import Enrollment
from CanvasSystem.Term import Term


def gather_emrollment_terms(settings, canvas, terms_file, encryption_obj):
    if settings.PULL_FROM_SERVER and settings.PULL_TERMS_FROM_SERVER:
        terms = canvas.get_all_terms()
        # remove any duplicates that got into the system
        term_dict = {}
        for term in terms:
            term_dict[term.id] = term
        terms = [v for k, v in term_dict.items() if not (v.start_date is None or v.end_date is None)]
        terms.sort()
        with open(terms_file, 'w') as file:
            file.write('id,name,start_date,end_date,is_available\n')
            for term in terms:
                if settings.ENCYRPT_DATA:
                    term.encrypt(encryption_obj)
                file.write(term.as_csv_line())
    else:
        terms = []
        with open(terms_file) as file:
            lines = file.readlines()
            for line in lines[1:]:
                terms.append(Term(line, in_as='csv'))

    min_date = None
    max_date = None
    for term in terms:
        if settings.ENCYRPT_DATA:
            term.decrypt(encryption_obj)
        # if term.start_date or term.end_date > time.time()
        if min_date is None or term.start_date < min_date:
            min_date = term.start_date
        if max_date is None or term.end_date > max_date:
            max_date = term.end_date

    term_dict = {}
    for term in terms:
        term_dict[term.id] = term

    return terms


def gather_courses(settings, canvas, terms, courses_file, encryption_obj):
    courses = []
    if settings.PULL_FROM_SERVER and settings.PULL_COURSES_FROM_SERVER:
        courses = canvas.get_all_courses_in_terms(terms)
        with open(courses_file, 'w') as file:
            file.write('term_id,id,name,course_level,credit_count,start_date,end_date\n')
            for course in courses:
                if settings.ENCYRPT_DATA:
                    course.encrypt(encryption_obj)
                file.write(course.as_csv_line())
    else:
        with open(courses_file) as file:
            lines = file.readlines()[1:]
            for line in lines:
                courses.append(Course(line, in_as='csv'))
    if settings.ENCYRPT_DATA:
        for course in courses:
            course.decrypt(encryption_obj)
    crs_dict = {}
    for course in courses:
        if course.id not in crs_dict:
            crs_dict[course.id] = course

    return courses, crs_dict


def gather_enrollments(settings, canvas, courses, enrollment_file, encryption_obj):
    enrollments = []
    if settings.PULL_FROM_SERVER and settings.PULL_ENROLLMENTS_FROM_SERVER:
        enrollments = canvas.get_all_course_enrollments(courses)
        with open(enrollment_file, 'w') as file:
            file.write('term_id,course_id,student_id\n')
            for enrollment in enrollments:
                if settings.ENCYRPT_DATA:
                    enrollment.encrypt(encryption_obj)
                file.write(enrollment.as_csv_line())
    else:
        with open(enrollment_file) as file:
            lines = file.readlines()[1:]
            for line in lines:
                enrollments.append(Enrollment(line, in_as='csv'))
    if settings.ENCYRPT_DATA:
        for enrollment in enrollments:
            enrollment.decrypt(encryption_obj)

    return enrollments
