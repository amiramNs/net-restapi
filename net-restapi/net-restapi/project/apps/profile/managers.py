from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, first_name=None, last_name=None, **extra_fields):
        user = self.model(username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        super_user = self.create_user(username, password=password, first_name='Admin', last_name='Admin', **extra_fields)
        super_user.set_password(password)
        super_user.first_name = f'Admin-{super_user.id}'
        super_user.last_name = f'Admin-{super_user.id}'
        super_user.save()

        return super_user
