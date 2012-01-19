from userroles.models import UserRole
from userroles.tests import roles


class CustomUserRole(UserRole):
    """
    Custom user role class to test 'USER_ROLE_CLASS' setting.
    """

    # Play nicely with project we're installed into, by using our custom
    # test roles for our UserRole class, rather than the default global roles,
    # loaded from the project settings.
    valid_roles = roles

    @property
    def can_moderate_discussions(self):
        return self.is_moderator or self.is_manager
