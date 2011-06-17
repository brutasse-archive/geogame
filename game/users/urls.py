from django.conf.urls.defaults import patterns, include, url

from users import views


urlpatterns = patterns('',
    url(r'^authorize/$', views.authorize, name='oauth_authorize'),
    url(r'^callback/$', views.callback, name='oauth_callback'),
)
