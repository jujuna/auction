from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_length(value):
    if len(str(value)) != 11:
        raise ValidationError(
            _('პირადობა 11 ციფრიანია!')
        )




class MyUserManager(BaseUserManager):
    def create_user(self, username, email, phone, address, last_name, first_name, passport_id, password=None):
        if not username:
            raise ValueError('მეტსახელი აუცილებელია')
        if not email:
            raise ValueError('მეილი აუცილებელია')
        elif not phone:
            raise ValueError('ტელეფონის ნომრის შევსება აუცილებელია')
        elif not address:
            raise ValueError('მისამართი აუცილებელია')
        elif not last_name:
            raise ValueError('გვარი აუცილებელია')
        elif not first_name:
            raise ValueError('სახელი აუცილებელია')
        elif not passport_id:
            raise ValueError('პირადი ნომერი აუცილებელია')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            address=address,
            last_name=last_name,
            first_name=first_name,
            passport_id=passport_id
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, verbose_name=_('მეტსახელი'), error_messages={'unique': 'ასეთი მეტსახელი არსებობს'})
    email = models.EmailField(unique=True, verbose_name=_('მეილი'), error_messages={'unique': 'ეს მაილი უკვე გამოყენებულია'})
    phone = models.CharField(max_length=30, validators=[RegexValidator(regex=r'^[5]\d{8}', message=_('უნდა იწყებოდეს 5-ზე და იყოს 9 ციფრიანი'))], verbose_name=_('ტელეფონის ნომერი'))
    balance = models.IntegerField(verbose_name=_('ბალანსი'),default=0)
    address = models.CharField(max_length=50, verbose_name=_('მისამართი'))
    first_name = models.CharField(max_length=20, verbose_name=_('სახელი'))
    last_name = models.CharField(max_length=25, verbose_name=_('გვარი'))
    passport_id = models.BigIntegerField(validators=[validate_length], verbose_name=_('პირადი ნომერი'))


    object = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('მომხმარებელი')

    def __str__(self):
        return self.email

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
