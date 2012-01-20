from django.db import models


class ModeratorProfile(models.Model):
    stars = models.IntegerField()
