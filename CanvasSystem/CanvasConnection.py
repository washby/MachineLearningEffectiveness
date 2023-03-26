import json
import random
import string
from datetime import datetime
from os import listdir
from os.path import join

import requests

from CanvasSystem.Course import Course
from CanvasSystem.Enrollment import Enrollment
from CanvasSystem.Term import Term


class CanvasSystem:
    def __init__(self, filename, api_url_ext='/api/v1/'):
        self.OVERFLOW_DIR = 'overflow_files'
        self.DUMP_LIST_OVERFLOW_LIMIT = 1000
        self.__config_info = None
        with open(filename) as file:
            self.__config_info = json.load(file)

        if self.__config_info is not None:
            self.__name = self.__config_info['name']
            self.__base_url = f"{self.__config_info['base_url']}{api_url_ext}"
            self.__api_token = self.__config_info['api_token']
            self.__headers = {"Authorization": f"Bearer {self.__api_token}"}
            self.__account_id = self.__config_info['account_id']

    def get_all_terms(self):
        api_suffix = f"accounts/{self.__account_id}/terms"
        response = self.__get_canvas_response(api_suffix, "terms")
        results = []
        while response.links.get("next", {}).get("url"):
            terms = json.loads(response.content)
            for term in terms['enrollment_terms']:
                results.append(Term(term))
            response = requests.get(response.links.get("next", {}).get("url"), headers=self.__headers)
        for term in terms['enrollment_terms']:
            results.append(Term(term))
        return results

    def get_all_courses_in_terms(self, terms_list):
        random_prefix = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
        used_overflow = False
        if not isinstance(terms_list, list):
            return TypeError(f"term_list is not instance of list it is {type(terms_list)}.")
        api_suffix = f"accounts/{self.__account_id}/courses"
        results = []
        for term in terms_list:
            print(f'Getting courses for {term}')
            ep = {"enrollment_term_id": term.id}
            response = self.__get_canvas_response(api_suffix, "courses", extra_params=ep)
            next_url = response.links.get("next", {}).get("url")
            while next_url:
                courses = json.loads(response.content)
                for course in courses:
                    if course['sis_course_id'] is not None:
                        results.append(Course(course))
                        if len(results) >= self.DUMP_LIST_OVERFLOW_LIMIT:
                            self.__dump_to_overflow(random_prefix, results, "course")
                            used_overflow = True
                            results = []
                response = self.__get_canvas_response(next_url, "courses", extra_params=ep, is_next_url=True)
                next_url = response.links.get("next", {}).get("url")
            courses = json.loads(response.content)
            for course in courses:
                if course['sis_course_id'] is not None:
                    results.append(Course(course))
            print(f'There are current {len(results)} courses in results')
        if used_overflow:
            print("------------------------------USED OVERFLOW----------------------------------------------------")
            with open(join(self.OVERFLOW_DIR, f'{random_prefix}courses-overflow-{date_str}.csv'), 'a') as outfile:
                for item in results:
                    outfile.write(item.as_csv_line())
            results = []
            files_with_prefix = []
            for filename in listdir(self.OVERFLOW_DIR):
                if filename.startswith(random_prefix) and filename.endswith('.csv'):
                    with open(join(self.OVERFLOW_DIR, filename)) as file:
                        for line in file.readlines():
                            results.append(Course(line, in_as='csv'))
        return results

    def __dump_to_overflow(self, random_prefix, results, obj):
        used_overflow = True
        date_str = str(datetime.utcnow()).replace(':', '.')
        filename = f'{random_prefix}{obj}-overflow-{date_str}.csv'
        with open(join(self.OVERFLOW_DIR, filename), 'a') as outfile:
            for item in results:
                outfile.write(item.as_csv_line())
        return date_str, used_overflow

    # noinspection DuplicatedCode
    def get_all_course_enrollments(self, course_list):
        random_prefix = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
        used_overflow = False
        if not isinstance(course_list, list):
            return TypeError(f"course_list is not instance of list it is {type(course_list)}.")
        results = []
        len_of_course_list = len(course_list)
        for i, course in enumerate(course_list):
            print(f'{i+1} of {len_of_course_list}) Getting enrollments for {course} with id=', end='')
            print(f'{course.id} in term id of {course.term_id}')
            ep = {"enrollment_type": "student"}
            api_suffix = f"courses/{course.id}/search_users"
            response = self.__get_canvas_response(api_suffix, "courses", extra_params=ep)
            next_url = response.links.get("next", {}).get("url")
            while next_url:
                student_enrollments = json.loads(response.content)
                for student in student_enrollments:
                    results.append(Enrollment(student, course_id=course.id, term_id=course.term_id))
                    if len(results) >= self.DUMP_LIST_OVERFLOW_LIMIT:
                        self.__dump_to_overflow(random_prefix, results, "enrollment")
                        used_overflow = True
                        results = []
                response = self.__get_canvas_response(next_url, "enrollment", extra_params=ep, is_next_url=True)
                next_url = response.links.get("next", {}).get("url")
            student_enrollments = json.loads(response.content)
            for student in student_enrollments:
                results.append(Enrollment(student, course_id=course.id, term_id=course.term_id))
        if used_overflow:
            print("------------------------------USED OVERFLOW----------------------------------------------------")
            self.__dump_to_overflow(random_prefix, results, "enrollment")
            results = []
            for filename in listdir(self.OVERFLOW_DIR):
                if filename.startswith(random_prefix) and filename.endswith('.csv'):
                    with open(join(self.OVERFLOW_DIR, filename)) as file:
                        for line in file.readlines():
                            results.append(Course(line, in_as='csv'))
        return results

    def __get_canvas_response(self, url_info, search_item, extra_params=None, is_next_url=False):
        if self.__config_info is None:
            raise Exception("The CanvasSystem class has not been initialized properly.")
        params = None
        if not is_next_url:
            url = f'{self.__base_url}{url_info}'
            params = {'per_page': 100}
            if extra_params:
                if not isinstance(extra_params, dict):
                    raise TypeError("Extra parameters needs to be passed in as dictionary.")
                for key in extra_params.keys():
                    params[key] = extra_params[key]
            response = requests.get(url, headers=self.__headers, params=params)
        else:
            url = url_info
            response = requests.get(url, headers=self.__headers)
        if response.status_code != 200:
            print(f"Failed to retrieve {search_item} from Canvas LMS with response code {response.status_code}", end='')
            print(f' on url {url}')
            exit()
        return response


