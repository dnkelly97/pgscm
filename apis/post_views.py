from django.shortcuts import render
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from apis.permissions import HasAPIKey
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes, permission_classes
from .models import *
from django.http.response import JsonResponse
from .serializers import StudentSerializer
from student.models import Student
from rest_framework import status


@api_view(['POST', 'PUT'])
@parser_classes([JSONParser])
@permission_classes([HasAPIKey])
def json_view(request, format=None):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    api_key = APIKey.objects.get_from_key(key)

    if request.method == 'POST':
        if api_key != None:
            serializer = StudentSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse("No API In Database", safe=False, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if api_key != None:
            serializer = StudentSerializer(data=request.data, many=True)
            if serializer.is_valid():
                print(serializer.validated_data[0]['email'])
                email = serializer.validated_data[0]['email']
                student_list = Student.objects.filter(email=email)
                if not student_list:
                    serializer.save()
                else:
                    student = student_list[0]
                    serializer = StudentSerializer(student)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse("No API In Database", safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([HasAPIKey])
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
