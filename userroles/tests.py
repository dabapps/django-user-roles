"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase
from django.test.utils import override_settings

from milkman.dairy import milkman
#from userroles.models import UserRole


class ManagerRole(models.Model):
    star_rating = models.IntegerField(default=3)


class ClientRole(models.Model):
    foobar = models.CharField(max_length=32)

    #@property
    #def custom_propery(self):
    #    return True


class SimpleTest(TestCase):
    @override_settings(USER_ROLES=(('manager', ''),))
    def test_creating_user_creates_role(self):
        user = milkman.deliver(User)
        self.assertEquals(user.role, 'manager')

    @override_settings(USER_ROLES=(('manager', 'userroles.tests.ManagerRole'),))
    def test_custom_role_information(self):
        user = milkman.deliver(User)
        self.assertEquals(user.role.star_rating, 3)

    #@override_settings(USER_ROLES=(('manager', 'userroles.tests.ManagerRole'),
    #                                ('client', 'userroles.tests.ClientRole')))
    #def test_create_user_role(self):
    #    UserRole('client', foobar='baz')
