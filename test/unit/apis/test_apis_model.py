import pytest
from apis.models import APIKey
from django.core import mail

@pytest.mark.django_db
def test_api_create():
   length = len(APIKey.objects.all())
   obj = APIKey(
       name="tester",
       email="tester@uiowa.edu",

   )
   APIKey.objects.assign_key(obj)
   obj.save()

   assert obj.email == "tester@uiowa.edu"
   assert obj.name == "tester"
   assert len(obj.prefix) == 8
   assert len(obj.hashed_key) == 78
   assert length+1 == len(APIKey.objects.all())
   assert obj.revoked == False
   assert obj.expiry_date == None

@pytest.mark.django_db
def test_api_email():
   obj = APIKey(
      name="tester",
      email="tester@uiowa.edu",

   )
   key = APIKey.objects.assign_key(obj)
   object = obj.save()

   APIKey.send_email(object,key,obj.email)
   assert len(mail.outbox) == 1
   assert mail.outbox[0].subject, 'App Permissions'
