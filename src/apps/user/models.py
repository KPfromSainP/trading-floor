from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from utils.strings import email_normalization


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password, room_number, last_name=None):
        if not email:
            raise TypeError('The "email" field is required')
        if not first_name:
            raise TypeError('The "first name" field is required')
        if not password:
            raise TypeError('The "password" field is required')
        if not room_number:
            raise TypeError('The "room number" field is required')

        user = self.model(
            email=email_normalization(email),
            first_name=first_name,
            last_name=last_name,
            room_number=room_number,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password, room_number=666)
        user.is_superuser = True
        user.save()

        return user


class ActiveUsersManager(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20)
    room_number = models.PositiveIntegerField('Номер комнаты')
    avatar = ProcessedImageField(
        format='PNG',
        processors=[
            ResizeToFill(50, 50),
        ],
        verbose_name='Аватарка пользователя',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'password']

    objects = ActiveUsersManager.as_manager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
