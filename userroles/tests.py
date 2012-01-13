"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings

from milkman.dairy import milkman


class SimpleTest(TestCase):
    @override_settings(USER_ROLES=('manager', ''))
    def test_creating_user_creates_role(self):
        user = milkman.deliver(User)
        self.assertEquals(user.role, 'manager')
