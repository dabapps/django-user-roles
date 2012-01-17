"""
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
from userroles.models import UserRole, set_user_role
from userroles import roles


class RoleObjectTests(TestCase):
    def test_existing_role_propery(self):
        self.assertTrue(roles.manager)

    def test_non_existing_role_propery(self):
        self.assertRaises(AttributeError, getattr, roles, 'foobar')


# Basic user role tests

class Dummy(object):
    pass


class ManagerRole(models.Model):
    star_rating = models.IntegerField(default=3)


class RoleTests(TestCase):
    """
    Test basic role operations.
    """

    def setUp(self):
        user = milkman.deliver(User)
        set_user_role(user, roles.manager)
        self.user = User.objects.get(id=user.id)

    def test_role_comparison(self):
        """
        Ensure that we can test if a user role has a given value.
        """
        self.assertEquals(self.user.role, roles.manager)

    def test_role_in_set(self):
        """
        Ensure that we can test if a user role exists in a given set.
        """
        self.assertIn(self.user.role, (roles.manager,))

    def test_invalid_role(self):
        """
        Ensure that trying to get an invalid role raises an attribute error.
        """
        self.assertRaises(AttributeError, getattr, roles, 'foobar')


# Tests for user role view decorators

urlpatterns = patterns('userroles.tests',
    (r'^manager_or_moderator$', 'manager_or_moderator'),
)


@role_required(roles.manager, roles.moderator)
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
        set_user_role(self.user, roles.manager)
        resp = self.client.get('/manager_or_moderator')
        self.assertEquals(resp.status_code, 200)

    def test_get_disallowed_view(self):
        set_user_role(self.user, roles.client)
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
        set_user_role(self.user, roles.moderator)

    def tearDown(self):
        if not self.orig_role_class:
            del settings.USER_ROLE_CLASS
        else:
            settings.USER_ROLE_CLASS = self.orig_role_class

    def test_role_has_custom_property(self):
        self.assertTrue(self.user.role.can_moderate_discussions)
