from django.db import models
from userroles.models import UserRole


class TestModeratorProfile(UserRole):
    stars = models.IntegerField()
