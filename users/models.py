from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'Role'


class MyUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='users')
    password = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    class Meta:
        db_table = 'User'

    def save(self, *args, **kwargs):
        if self.role_id == 1:
            self.is_staff = True
        super().save(*args, **kwargs)
