from django.conf.urls import patterns, url

urlpatterns = patterns('app.views',
    url(r'^$', 'index', name='index'),
    url(r'^check-point/$', 'check_point', name='check_point'),
)