from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Hit.views.home', name='home'),
    url(r'^signup/$', 'Hit.views.signup', name='signup'),
    url(r'^login/$', 'Hit.views.login', name='login'),
    url(r'^plan/$', 'activity.views.plan', name='plan'),
    
    url(r'^p/', include('place.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
