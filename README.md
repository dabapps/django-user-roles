Django User Roles
=================

Simple role-based user permissions and profiles for Django.

django-user-roles is a reusable app that allows you to create a set of user roles,
which can be used to control which views each type of user has permission to view, and to customize how the site is presented to different types of user.

User roles can also be associated with differing profile classes, allowing you to store different types of user information for different user types.

Settings
--------

Install using `pip`:

	pip install django-user-roles

Add the `USER_ROLES` setting to your `settings.py`:

    USER_ROLES = (
        ('manager', 'myproject.ManagerUserProfile'),
        ('moderator', 'myproject.ModeratorUserProfile'),
        ('client', 'myproject.ClientUserProfile'),
    )

Basic Usage
-----------

Setting and checking the user role:

    user.role = 'manager'
    user.role == 'manager'
    user.role in ('manager', 'moderator')


The `role_required` decorator provides similar behavior to Django's `login_required` and `permission_required` decorators.  If the user accessing the view does not have the required roles, they will be redirected to the login page:

    from userroles.decorators import role_required

    @role_required('manager', 'moderator')
    def view(request):
        ...

Using Custom Role Classes
-------------------------

It can sometime be useful to override the default user role class.
You can do this by setting `USER_ROLE_CLASS` in your settings file.

`settings.py`:

    USER_ROLE_CLASS = 'myapp.models.CustomUserRole'

`models.py`:

    def CustomUserRole(userroles.UserRole):
        @property
        def can_moderate_discussions(self):
            return self in ('manager', 'moderator')

`views.py`:

	def view(request):
        if user.role.can_moderate_discussions:
            ...
		else:
			...

Testing
-------

./manage.py test userroles
