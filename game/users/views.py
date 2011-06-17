from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson as json

from le_social.twitter import views

import twitter

from users.models import Twitter


class Authorize(views.Authorize):
    def build_callback(self):
        protocol = 'https' if self.request.is_secure() else 'http'
        return '%s://%s%s' % (protocol,
                              RequestSite(self.request).domain,
                              reverse('oauth_callback'))
authorize = Authorize.as_view()


class Callback(views.Callback):
    def error(self, message, exception=None):
        return HttpResponse(message)

    def success(self, auth):
        api = twitter.Twitter(auth=auth)
        user = api.account.verify_credentials()
        try:
            dbuser = User.objects.get(username=user['screen_name'])
        except User.DoesNotExist:
            dbuser = User.objects.create_user(
                user['screen_name'],
                user['screen_name'] + '@twitter.com',
                '!',
            )
            dbuser.set_unusable_password()
            dbuser.save()
        try:
            dbuser.twitter
        except Twitter.DoesNotExist:
            Twitter.objects.create(
                user=dbuser,
                username=user['screen_name'],
                token=auth.token,
                token_secret=auth.token_secret,
                profile=json.dumps(user),
            )
        dbuser.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, dbuser)
        return redirect(reverse('question'))
callback = Callback.as_view()
