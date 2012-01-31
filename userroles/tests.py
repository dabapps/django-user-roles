"""
"""

from django.conf import settings
from django.contrib.auth.models import User
from milkman.dairy import milkman
from userroles.models import set_user_role, UserRole
from userroles.testapp.models import TestModeratorProfile
from userroles.utils import SettingsTestCase
from userroles import Roles

# Test setup

roles_config = (
    'manager',
    'moderator',
    'client',
)

installed_apps_config = list(settings.INSTALLED_APPS)
installed_apps_config.append('userroles.testapp')

roles = Roles(roles_config)


class TestCase(SettingsTestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.settings(
            INSTALLED_APPS=installed_apps_config,
            ROOT_URLCONF='userroles.testapp.urls',
            USER_ROLES=roles_config
        )
        self.restore_roles = UserRole._valid_roles
        UserRole._valid_roles = roles

    def tearDown(self):
        UserRole._valid_roles = self.restore_roles


class DummyClass(object):
    pass


# Basic user role tests

class RoleTests(TestCase):
    """
    Test operations on role object.
    """

    def test_existing_role_propery(self):
        """
        Ensure that we can get a valid role.
        """
        self.assertTrue(roles.manager)

    def test_non_existing_role_propery(self):
        """
        Ensure that trying to get an invalid role raises an attribute error.
        """
        self.assertRaises(AttributeError, getattr, roles, 'foobar')


class UserRoleTests(TestCase):
    """
    Test basic user.role operations.
    """

    def setUp(self):
        super(UserRoleTests, self).setUp()
        self.user = milkman.deliver(User)
        set_user_role(self.user, roles.manager)

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

    def test_is_role(self):
        """
        Test `user.role.is_something` style.
        """
        self.assertTrue(self.user.role.is_manager)

    def test_is_not_role(self):
        """
        Test `user.role.is_not_something` style.
        """
        self.assertFalse(self.user.role.is_moderator)

    def test_is_invalid_role(self):
        """
        Test `user.role.is_invalid` raises an AttributeError.
        """
        self.assertRaises(AttributeError, getattr, self.user.role, 'is_foobar')

    def test_set_role_without_profile(self):
        """
        Set a role that does not take a profile.
        """
        set_user_role(self.user, roles.client)
        self.assertTrue(self.user.role.is_client)

    def test_set_role_with_profile(self):
        """
        Set a role that takes a profile.
        """
        set_user_role(self.user, roles.moderator, TestModeratorProfile(stars=5))
        self.assertTrue(self.user.role.is_moderator)
        self.assertEquals(self.user.role.profile.stars, 5)

    # def test_set_role_without_profile_incorrectly(self):
    #     """
    #     Attempt to set a profile on a role that does not take a profile.
    #     """
    #     args = (self.user, roles.client, ModeratorProfile())
    #     self.assertRaises(ValueError, set_user_role, *args)

    # def test_set_role_with_profile_incorrectly(self):
    #     """
    #     Attempt to set a role that uses profiles, without setting a profile.
    #     """
    #     args = (self.user, roles.moderator, )
    #     self.assertRaises(ValueError, set_user_role, *args)

    # def test_set_role_with_profile_using_wrong_profile(self):
    #     """
    #     Attempt to set a role that uses profiles, without setting a profile.
    #     """
    #     args = (self.user, roles.moderator, DummyClass())
    #     self.assertRaises(ValueError, set_user_role, *args)


# Tests for user role view decorators

class ViewTests(TestCase):
    def setUp(self):
        super(ViewTests, self).setUp()
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

# class UserRoleClassSettingTests(TestCase):
#     def setUp(self):
#         super(UserRoleClassSettingTests, self).setUp()
#         self.user = milkman.deliver(User)
#         set_user_role(self.user, roles.moderator)

#     def test_role_has_custom_property(self):
#         self.assertTrue(self.user.role.can_moderate_discussions)
