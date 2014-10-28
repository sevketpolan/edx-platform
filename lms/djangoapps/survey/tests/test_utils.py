"""
Python tests for the Survey models
"""

from collections import OrderedDict

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from survey.models import SurveyForm

from xmodule.modulestore.tests.factories import CourseFactory

from survey.utils import is_survey_required_for_course, has_user_answered_required_survey_for_course


class SurveyModelsTests(TestCase):

    def setUp(self):
        """
        Set up the test data used in the specific tests
        """
        self.client = Client()

        # Create two accounts
        self.password = 'abc'
        self.student = User.objects.create_user('student', 'student@test.com', self.password)
        self.student2 = User.objects.create_user('student2', 'student2@test.com', self.password)

        self.test_survey_name = 'TestSurvey'
        self.test_form = '<input></input>'
        self.test_form_update = '<input>updated</input>'

        self.student_answers = OrderedDict({
            'field1': 'value1',
            'field2': 'value2',
        })

        self.student2_answers = OrderedDict({
            'field1': 'value3'
        })

        self.course = CourseFactory.create(
                    course_survey_required=True,
                    course_survey_name=self.test_survey_name
                )

        self.survey = SurveyForm.create(self.test_survey_name, self.test_form)

    def test_is_survey_required_for_course(self):
        """
        Assert the a requried course survey is when both the flags is set and a survey name
        is set on the course descriptor
        """
        self.assertTrue(is_survey_required_for_course(self.course))

    def test_is_survey_no_required_for_course(self):
        """
        Assert that if various data is not available or if the survey is not found
        then the survey is not considered required
        """
        course = CourseFactory.create()
        self.assertFalse(is_survey_required_for_course(course))

        course = CourseFactory.create(
            course_survey_required=False
        )
        self.assertFalse(is_survey_required_for_course(course))

        course = CourseFactory.create(
            course_survey_required=True,
            course_survey_name="NonExisting"
        )
        self.assertFalse(is_survey_required_for_course(course))

    def test_user_not_yet_answered_required_survey(self):
        """
        Assert that a new course which has a required survey but user has not answered it yet
        """
        self.assertFalse(has_user_answered_required_survey_for_course(self.course, self.student))

        temp_course = CourseFactory.create(
            course_survey_required=False
        )
        self.assertFalse(has_user_answered_required_survey_for_course(temp_course, self.student))

        temp_course = CourseFactory.create(
            course_survey_required=True,
            course_survey_name="NonExisting"
        )
        self.assertFalse(has_user_answered_required_survey_for_course(temp_course, self.student))

    def test_user_has_answered_required_survey(self):
        """
        Assert that a new course which has a required survey and user has answers for it
        """
        self.survey.save_user_answers(self.student, self.student_answers)
        self.assertTrue(has_user_answered_required_survey_for_course(self.course, self.student))


