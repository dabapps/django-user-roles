from django.conf.urls.defaults import patterns

urlpatterns = patterns('userroles.testapp.views',
    (r'^manager_or_moderator$', 'manager_or_moderator'),
)
