"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.exceptions import ValidationError
from django.conf import settings
from django.conf.urls import patterns
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse
from django.test import TestCase

from milkman.dairy import milkman

from userroles.decorators import role_required
from userroles.models import UserRole

#class ManagerRole(models.Model):
#    star_rating = models.IntegerField(default=3)


#class ClientRole(models.Model):
#    foobar = models.CharField(max_length=32)


# Basic user role tests

class RoleTests(TestCase):
    """
    Test basic role operations - getting, setting and comparisons.
    """

    def setUp(self):
        self.user = milkman.deliver(User)

    def reload_user(self):
        return User.objects.get(id=self.user.id)

    def test_set_valid_user_role(self):
        """
        Ensure that we can set user roles to a valid value.
        """
        self.user.role = 'manager'
        self.assertEquals(self.reload_user().role, 'manager')

    def test_set_invalid_user_role(self):
        """
        Ensure that we cannot set user roles to an invalid value.
        """
        args = (self.user, 'role', 'foobar')
        self.assertRaises(ValidationError, setattr, *args)

    def test_default_user_role(self):
        """
        Ensure that user roles have a valid value when unset.
        """
        self.assertEquals(self.reload_user().role, 'manager')

    def test_role_exists_in_set(self):
        """
        Ensure that we can test if a user role exists in a given set.
        """
        self.user.role = 'manager'
        self.assertIn(self.reload_user().role, ('manager',))


# Tests for user role view decorators

urlpatterns = patterns('userroles.tests',
    (r'^manager_or_moderator$', 'manager_or_moderator'),
)


@role_required('manager', 'moderator')
def manager_or_moderator(request):
    return HttpResponse('ok')


class ViewTests(TestCase):
    urls = 'userroles.tests'

    def setUp(self):
        self.user = milkman.deliver(User)
        self.user.set_password('password')
        self.user.save()
        self.client.login(username=self.user.username, password='password')

    def test_get_allowed_view(self):
        self.user.role = 'moderator'
        resp = self.client.get('/manager_or_moderator')
        self.assertEquals(resp.status_code, 200)

    def test_get_disallowed_view(self):
        self.user.role = 'client'
        resp = self.client.get('/manager_or_moderator')
        self.assertEquals(resp.status_code, 302)


# Tests for using a custom UserRole class

class CustomUserRole(UserRole):
    @property
    def can_moderate_discussions(self):
        return self in ('moderator', 'manager')


class UserRoleClassSettingTests(TestCase):
    def setUp(self):
        # Note: If we move to Django 1.4, we can use proper test settings here.
        self.orig_role_class = getattr(settings, 'USER_ROLE_CLASS', None)
        settings.USER_ROLE_CLASS = 'userroles.tests.CustomUserRole'
        self.user = milkman.deliver(User)
        self.user.role = 'moderator'

    def tearDown(self):
        if not self.orig_role_class:
            del settings.USER_ROLE_CLASS
        else:
            settings.USER_ROLE_CLASS = self.orig_role_class

    def test_role_has_custom_property(self):
        self.assertTrue(self.user.role.can_moderate_discussions)


#    def setUp(self):
#        self.orig_settings = settings

#    def tearDown(self):


# class SimpleTest(TestCase):
#     @override_settings(USER_ROLES=(('manager', ''),))
#     def test_creating_user_creates_role(self):
#         user = milkman.deliver(User)
#         self.assertEquals(user.role, 'manager')

#     @override_settings(USER_ROLES=(('manager', 'userroles.tests.ManagerRole'),))
#     def test_get_custom_role_information(self):
#         user = milkman.deliver(User)
#         self.assertEquals(user.role.star_rating, 3)
