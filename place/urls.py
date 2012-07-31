from django.conf.urls import patterns, include, url

urlpatterns = patterns('place.views',
    url(r'^$', 'home', name='place-home'),
    url(r'^(?P<pid>\w+)$', 'profile', name='place-profile'),
    url(r'^search/', 'search', name='search'),
)