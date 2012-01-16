"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.conf.urls import patterns
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse
from django.test import TestCase
from django.test.utils import override_settings

from milkman.dairy import milkman

from userroles.decorators import user_has_role

urlpatterns = patterns('userroles.tests',
    (r'^manager_only_view$', 'manager_only_view'),
)


@user_has_role('manager')
def manager_only_view(request):
    return HttpResponse('ok')


class ManagerRole(models.Model):
    star_rating = models.IntegerField(default=3)


class ClientRole(models.Model):
    foobar = models.CharField(max_length=32)


class SimpleTest(TestCase):
    @override_settings(USER_ROLES=(('manager', ''),))
    def test_creating_user_creates_role(self):
        user = milkman.deliver(User)
        self.assertEquals(user.role, 'manager')

    @override_settings(USER_ROLES=(('manager', 'userroles.tests.ManagerRole'),))
    def test_get_custom_role_information(self):
        user = milkman.deliver(User)
        self.assertEquals(user.role.star_rating, 3)


class ViewTests(TestCase):
    urls = 'userroles.tests'

    def test_get(self):
        user = milkman.deliver(User)
        #user.role = ManagerRole()
        self.client.get('/manager_only_view')

    #@override_settings(USER_ROLES=(('manager', 'userroles.tests.ManagerRole'),
    #                                ('client', 'userroles.tests.ClientRole')))
    #def test_create_user_role(self):
    #    RoleProfile('client', foobar='baz')
