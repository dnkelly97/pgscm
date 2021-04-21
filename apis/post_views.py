from django.shortcuts import render
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from apis.permissions import HasAPIKey
from rest_framework.decorators import api_view, action
from rest_framework.decorators import parser_classes, permission_classes
from .models import *
from django.http.response import JsonResponse
from .serializers import StudentSerializer
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView


class CreateStudents(APIView):

    throttle_classes = ['1/min']

    @api_view(['POST'])
    @parser_classes([JSONParser])
    @permission_classes([HasAPIKey])
    @action(detail=True, methods=["post"], throttle_classes=['1/min'])
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
    @action(detail=True, methods=["post"], throttle_classes=[AnonRateThrottle])
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
