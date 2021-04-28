from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, name):
        if not id:
            raise ValueError('Customer must have all necessary information')
        user = CustomUser(name=name)
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, name, password):
        user = self.create_user(name=name)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Position(models.Model):
    position = models.CharField(max_length=255, verbose_name='Должность')

    def __str__(self):
        return self.position


class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=255, unique=True)

    position = models.ManyToManyField(Position, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'name'
    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True
