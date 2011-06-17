import math

from django.contrib.auth.models import User
from django.db import models


class Twitter(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    token_secret = models.CharField(max_length=255)
    profile = models.TextField()
    # Right answer: +2; wrong answer: -3
    score = models.IntegerField(db_index=True, default=0)

    def __unicode__(self):
        return u'%s' % self.username

    @property
    def level(self):
        """
        Very clever way to infer a user's level.
        """
        computed = float(self.score) / 50 + 1
        if computed < 1:
            return 1
        if computed > 5:
            return 5
        return int(computed)
