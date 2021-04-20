from django.db import models
from rest_framework_api_key.models import AbstractAPIKey
from rest_framework_api_key.crypto import KeyGenerator
from rest_framework_api_key.models import BaseAPIKeyManager
from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPException

# Create your models here.
class APIKeyManager(BaseAPIKeyManager):
    key_generator = KeyGenerator(prefix_length=8, secret_key_length=32)

class APIKey(AbstractAPIKey):
    objects = APIKeyManager()
    email = models.EmailField(max_length=255, unique=True)


    def send_email(self,key,email):
        try:
            send_mail(subject="App Permissions",
                      message="Your API key is: " + key + "\n\n" +
                              "This will only be sent to you once, so please store in a safe place." +
                              "If your API key expires or you lose it, please contact the Admin immediately.",
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[email],
                      fail_silently=False)

        except SMTPException as e:
            print('There was an error sending an email.' + str(e))
