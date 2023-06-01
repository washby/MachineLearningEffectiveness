class Settings:
    def __init__(self, pull_override, pull_terms, pull_courses, pull_enrollments, encrypt):
        self.PULL_FROM_SERVER = pull_override
        self.PULL_TERMS_FROM_SERVER = pull_terms
        self.PULL_COURSES_FROM_SERVER = pull_courses
        self.PULL_ENROLLMENTS_FROM_SERVER = pull_enrollments
        self.ENCYRPT_DATA = encrypt

