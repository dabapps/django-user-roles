Django User Roles
=================

Role-based user profiles for Django.


Django User Profiles is a reusable app that allows you to assign users to
fixed 

A User role:

1.  May have a set of user information applicable to that role that varies
    between roles.
2.  


Settings
--------

USER_ROLES = (
    ('manager', 'myproject.ManagerUserProfile'),
    ('moderator', 'myproject.ModeratorUserProfile'),
    ('client', 'myproject.ClientUserProfile'),
)

Usage
-----

Setting and checking the user role:

    user.role = 'manager'
    user.role == 'manager'
    user.role in ('manager', 'moderator')

View decorator similar to `login_required`, `permission_required`:

    @role_required('manager', 'moderator')
    def view(request):
        ...

Testing
-------

./manage.py test userroles
