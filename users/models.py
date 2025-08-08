from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone=None, email=None, password=None, **extra_fields):
        if not phone and not email:
            raise ValueError('Users must have either a phone number or an email')

        if email:
            email = self.normalize_email(email)
            extra_fields['email'] = email

        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone=phone, email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone or self.email or f'User {self.pk}'
