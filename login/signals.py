from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Administrator


def administrator_account(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='administrator')
        instance.groups.add(group)
        Administrator.objects.create(
            user=instance,
            name=instance.username,
        )
        print('Account created!')


post_save.connect(administrator_account, sender=User)
