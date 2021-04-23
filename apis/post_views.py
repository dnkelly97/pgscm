from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from apis.permissions import HasAPIKey
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes, permission_classes
from .models import *
from django.http.response import JsonResponse
from .serializers import StudentSerializer
from student.models import Student
from rest_framework import status


def get_object(email):
    try:
        return Student.objects.get(email=email)
    except (Student.DoesNotExist, ValidationError):
        return False


def validate_email(email_list):
    for email in email_list:
        try:
            Student.objects.get(email=email)
        except (Student.DoesNotExist, ValidationError):
            return False
    return True


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
        if api_key is not None:
            data = request.data
            email_list = [i['email'] for i in data]
            validate_email(email_list)
            instances = []
            for d in data:
                email = d['email']
                student = get_object(email)

                if student:
                    if 'first_name' in d:
                        student.first_name = d['first_name']
                    if 'last_name' in d:
                        student.last_name = d['last_name']
                    if 'school_year' in d:
                        student.school_year = d['school_year']
                    if 'research_interests' in d:
                        student.research_interests = d['research_interests']
                    if 'degree' in d:
                        student.degree = d['degree']
                    if 'university' in d:
                        student.university = d['university']
                    if 'gpa' in d:
                        student.gpa = d['gpa']
                    if 'ethnicity' in d:
                        student.ethnicity = d['ethnicity']
                    if 'gender' in d:
                        student.gender = d['gender']
                    if 'country' in d:
                        student.country = d['country']
                    if 'us_citizenship' in d:
                        student.us_citizenship = d['us_citizenship']
                    if 'first_generation' in d:
                        student.first_generation = d['first_generation']
                    if 'military' in d:
                        student.military = d['military']

                    student.save()
                    instances.append(student)

                else:
                    return JsonResponse("User not in database", safe=False, status=status.HTTP_400_BAD_REQUEST)

            serializer = StudentSerializer(instances, many=True)
            return JsonResponse(serializer.data, safe=False)

        else:
            return JsonResponse("No API In Database", safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([HasAPIKey])
def form_view(request, format=None):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    api_key = APIKey.objects.get_from_key(key)

    if request.method == 'POST':
        if api_key != None:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse("No API In Database", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if api_key is not None:
            data = request.data
            email_list = [i['email'] for i in data]
            validate_email(email_list)
            instances = []
            for d in data:
                email = d['email']
                student = get_object(email)

                if student:
                    if 'first_name' in d:
                        student.first_name = d['first_name']
                    if 'last_name' in d:
                        student.last_name = d['last_name']
                    if 'school_year' in d:
                        student.school_year = d['school_year']
                    if 'research_interests' in d:
                        student.research_interests = d['research_interests']
                    if 'degree' in d:
                        student.degree = d['degree']
                    if 'university' in d:
                        student.university = d['university']
                    if 'gpa' in d:
                        student.gpa = d['gpa']
                    if 'ethnicity' in d:
                        student.ethnicity = d['ethnicity']
                    if 'gender' in d:
                        student.gender = d['gender']
                    if 'country' in d:
                        student.country = d['country']
                    if 'us_citizenship' in d:
                        student.us_citizenship = d['us_citizenship']
                    if 'first_generation' in d:
                        student.first_generation = d['first_generation']
                    if 'military' in d:
                        student.military = d['military']

                    student.save()
                    instances.append(student)

                else:
                    return JsonResponse("User not in database", safe=False, status=status.HTTP_400_BAD_REQUEST)

            serializer = StudentSerializer(instances, many=True)
            return JsonResponse(serializer.data, safe=False)

        else:
            return JsonResponse("No API In Database", safe=False, status=status.HTTP_400_BAD_REQUEST)
