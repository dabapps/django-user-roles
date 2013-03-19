from django.contrib.auth.decorators import user_passes_test
from userroles.models import UserRole

def role_required(*roles):
    """
    Decorator for views that checks whether a user has a particular role,
    redirecting to the log-in page if neccesary.
    Follows same style as django.contrib.auth.decorators.login_required,
    and django.contrib.auth.decorators.permission_required.
    """
    def check_role(user):
        try:
            return getattr(user, 'role', None) in roles
        except UserRole.DoesNotExist:
            return False
    return user_passes_test(check_role)
