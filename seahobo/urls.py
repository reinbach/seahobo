from coffin.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

urlpatterns = patterns(
    '',
    (r'^robots.txt$', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}),
    url(r'^$', 'core.views.home', name='home'),
)

urlpatterns += staticfiles_urlpatterns()