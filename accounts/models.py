from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, role, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, role='receptionist', **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, role, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        role = 'admin'  # superusers are admins by default

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, role, **extra_fields)


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_RECEPTIONIST = 'receptionist'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_RECEPTIONIST, 'Receptionist'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_RECEPTIONIST)

    objects = UserManager()  # assign custom manager

    def save(self, *args, **kwargs):
        # Make sure role is admin if user is superuser
        if self.is_superuser:
            self.role = self.ROLE_ADMIN
        super().save(*args, **kwargs)

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_receptionist(self):
        return self.role == self.ROLE_RECEPTIONIST
