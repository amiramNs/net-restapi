from django.db import models
from django.contrib.auth.models import AbstractUser
from project.apps.profile.managers import UserManager


class User(AbstractUser):
    job = models.CharField(max_length=128, null=True, blank=True)
    email = None

    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def is_net_admin(self):
        return self.groups.filter(permissions__codename='user_admin').exists()

    @property
    def is_net_operator(self):
        return self.groups.filter(permissions__codename='user_operator').exists()

    @property
    def is_net_repair(self):
        return self.groups.filter(permissions__codename='user_repair').exists()



