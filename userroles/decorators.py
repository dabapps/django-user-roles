from django.contrib.auth.decorators import user_passes_test


def role_required(*roles):
    """
    Decorator for views that checks whether a user has a particular role,
    redirecting to the log-in page if neccesary.
    Follows same style as django.contrib.auth.decorators.login_required,
    and django.contrib.auth.decorators.permission_required.
    """
    def check_role(user):
        if not hasattr(user, 'role'):
	    return False
	return getattr(user, 'role', None) in roles
    return user_passes_test(check_role)
