import datetime

from django.contrib.auth.models import User
from django.db import models

from countries.models import Country


class AnonymousAccount(object):
    user = None

    def __init__(self, level):
        self.level = level


class Account(models.Model):
    user = models.OneToOneField(User)
    level = models.PositiveIntegerField(default=0)


class Question(models.Model):
    country = models.ForeignKey(Country, related_name='questions',
                                verbose_name='Country')
    left_choice = models.ForeignKey(Country, related_name='left_choices',
                                    verbose_name='Left Choice')
    right_choice = models.ForeignKey(Country, related_name='right_choices',
                                     verbose_name='Right Choice')
    answer = models.ForeignKey(Country, related_name='answers', null=True,
                               verbose_name='Answer')
    user = models.ForeignKey(User, related_name='questions', null=True,
                             verbose_name='User')
    date_created = models.DateTimeField('Date created',
                                        default=datetime.datetime.now)

    def wrong_answer(self):
        if self.country == self.left_choice:
            return self.right_choice
        else:
            return self.left_choice

    def __unicode__(self):
        return u'Question #%s' % self.pk
