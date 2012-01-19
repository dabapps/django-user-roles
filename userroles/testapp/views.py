from django.http import HttpResponse
from userroles.tests import roles
from userroles.decorators import role_required

# Note that we play nicely with project we're installed into, by using our
# custom test roles ('userroles.tests.roles'), rather than the default global
# roles, loaded from the project settings ('userroles.roles').


@role_required(roles.manager, roles.moderator)
def manager_or_moderator(request):
    """
    View to test the @role_required decorator.
    """
    return HttpResponse('ok')
