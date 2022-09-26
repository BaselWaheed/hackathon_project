from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.modelfields import PhoneNumberField


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google','twitter': 'twitter', 'email': 'email'}

class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False , unique=True)
    username = models.CharField(_("username"), max_length=70, unique=True )
    phone_number = PhoneNumberField(blank=True , null=True)
    auth_provider = models.CharField(max_length=255, blank=False,null=False, default=AUTH_PROVIDERS.get('email'))
    is_verified = models.BooleanField(_("verify") ,default=False)
    code = models.CharField(_("code"), max_length=50 , null=True , blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email

    def get_tokens_for_user(user):

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }












