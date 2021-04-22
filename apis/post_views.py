from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from apis.permissions import HasAPIKey
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.decorators import parser_classes, permission_classes
from .models import *
from django.http.response import JsonResponse
from .serializers import StudentSerializer
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView


class HundredPerDayThrottle(UserRateThrottle):
    rate = '100/day'

    def allow_request(self, request, view):
        if self.rate is None:
            return True
        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True
        self.history = self.cache.get(self.key, [])
        self.now = self.timer()
        email_list = []
        superusers = User.objects.filter(is_superuser=True)
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            for user in superusers:
                email_list.append(user.email)
            send_mail(subject="PGSCM rate limit exceeded", message=f"{self.get_ident(request)} exceeded the rate limit.", from_email='pgscm.uiowa@gmail.com', recipient_list=email_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
            naughty_key = APIKey.objects.get_from_key(request.META["HTTP_AUTHORIZATION"].split()[1])
            naughty_key.revoked = True
            naughty_key.save()
            return self.throttle_failure()
        return self.throttle_success()


class CreateStudents(APIView):

    @api_view(['POST'])
    @parser_classes([JSONParser])
    @permission_classes([HasAPIKey])
    @throttle_classes([HundredPerDayThrottle])
    def json_view(request, format=None):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = APIKey.objects.get_from_key(key)
        if api_key != None:
            serializer = StudentSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse("No API In Database", safe=False, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    @parser_classes([FormParser, MultiPartParser])
    @permission_classes([HasAPIKey])
    @throttle_classes([HundredPerDayThrottle])
    def form_view(request, format=None):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = APIKey.objects.get_from_key(key)
        if api_key != None:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse("No API In Database", status=status.HTTP_400_BAD_REQUEST)
