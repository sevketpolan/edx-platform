"""
Models to support Course Surveys feature
"""

import logging
from django.db import models
from student.models import User

from model_utils.models import TimeStampedModel

log = logging.getLogger("edx.survey")


class SurveyForm(TimeStampedModel):
    """
    Model to define a Survey Form that contains the HTML form data
    that is presented to the end user. A SurveyForm is not tied to
    a particular run of a course, to allow for sharing of Surveys
    across courses
    """
    name = models.CharField(max_length=255, db_index=True, unique=True)
    form = models.TextField()

    def __unicode__(self):
        return u'{}'.format(self.name)

    def get_all_answers(self):
        """
        Returns all answers for all users for this Survey
        """
        return SurveyAnswer.get_user_answers(self)

    def has_user_answered_survey(self, user):
        """
        Returns whether a given user has supplied answers to this
        survey
        """
        return SurveyAnswer.do_survey_answers_exist(self, user)


class SurveyAnswer(TimeStampedModel):
    """
    Model for the answers that a user gives for a particular form in a course
    """
    user = models.ForeignKey(User, db_index=True)
    form = models.ForeignKey(SurveyForm, db_index=True)
    field_name = models.CharField(max_length=255, db_index=True)
    field_value = models.CharField(max_length=1024)

    @classmethod
    def do_survey_answers_exist(cls, form, user):
        """
        Returns whether a user has any answers for a given SurveyForm for a course
        This can be used to determine if a user has taken a CourseSurvey.
        """
        return SurveyAnswer.objects.find(form=form, user=user).exists()

    @classmethod
    def get_answers(cls, form, user=None):
        """
        Returns all answers a user (or all users, when user=None) has given to an instance of a SurveyForm

        Return is a nested dict which are simple name/value pairs with an outer key which is the
        user id. For example (where 'field3' is an optional field):

        results = {
            '1': {
                'field1': 'value1',
                'field2': 'value2',
            },
            '2': {
                'field1': 'value3',
                'field2': 'value4',
                'field3': 'value5',
            }
            :
            :
        }
        """

        if user:
            answers = SurveyAnswer.objects.find(form=form, user=user)
        else:
            answers = SurveyAnswer.objects.find(form=form)

        results = dict()
        for answer in answers:
            user_id = answer.user__id
            if user_id not in results:
                results[user_id] = dict()

            results[user_id][answer.field_name] = answer.field_value

        return results

    @classmethod
    def save_answers(cls, form, user, answers):
        """
        Store answers to the form for a given user. Answers is a dict of simple
        name/value pairs

        IMPORTANT: There is no validaton of form answers at this point. All data
        supplied to this method is presumed to be previously validated
        """
        for name in answers.keys():
            value = answers[name]

            # See if there is an answer stored for this user, form, field_name pair or not
            # this will allow for update cases. This does include an additional lookup,
            # but write operations will be relatively infrequent
            answer, __ = SurveyAnswer.objects.get_or_create(user=user, form=form, field_name=name)
            answer.field_value = value
            answer.save()

    @classmethod
    def get_field_names(cls, form):
        """
        Returns a list of unique field names for a given Survey.
        This can be useful for formatting reports, e.g. putting table headers on each column
        """
        field_names = SurveyAnswer.objects.order_by('field_name').values('field_name').distinct()

        results = []
        for name in field_names:
            results.append(name)

            return results
