from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from apis.permissions import HasAPIKey
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.decorators import parser_classes, permission_classes
from .models import *
from django.http.response import JsonResponse
from .serializers import StudentSerializer, JSONStudentSerializer
from student.models import Student
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from enum import Enum


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
        if len(self.history) >= self.num_requests:  # pragma: no cover
            for user in superusers:
                email_list.append(user.email)
            send_mail(subject="PGSCM rate limit exceeded", message=f"{self.get_ident(request)} exceeded the rate limit.", from_email=settings.EMAIL_HOST_USER, recipient_list=email_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
            naughty_key = APIKey.objects.get_from_key(request.META["HTTP_AUTHORIZATION"].split()[1])
            naughty_key.revoked = True
            naughty_key.save()
            return self.throttle_failure()
        return self.throttle_success()


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

def json_data_formatter(student, errors=None):
    if errors:
        return {
            "errors": errors,
            "student": student
        }
    else:
        return {
            "student": student
        }

class CreateStudents(APIView):

    @staticmethod
    def return_result(data, type):
        bad_request = 400
        if type == 'POST':
            responses = {
                201: [],
                400: [],
                409: []
            }
            success = 201
            invalid = 409
        else:
            responses = {
                204: [],
                400: [],
                404: []
            }
            success = 204
            invalid = 404

        for student in data['students']:
            json_serializer = JSONStudentSerializer(data=student)
            if json_serializer.is_valid():
                student_serializer = StudentSerializer(data=student)
                if student_serializer.is_valid() and 'save_valid' in request.data and request.data['save_valid']:
                    student_serializer.save()
                    responses[success].append(json_data_formatter(student_serializer.data))
                else:
                    responses[invalid].append(json_data_formatter(student_serializer.data, student_serializer.errors))
            else:
                responses[bad_request].append(json_data_formatter(json_serializer.data, json_serializer.errors))

        if 'save_valid' in data and data['save_valid']:
            if responses[bad_request] == [] and responses[invalid] == []:
                return JsonResponse(responses[success], safe=False, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(responses, safe=False, status=status.HTTP_207_MULTI_STATUS)
        else:
            if responses[bad_request] == [] and responses[invalid] == []:
                serializer = StudentSerializer(data['students'], many=True)
                serializer.is_valid()
                serializer.save()
                responses[success] = serializer.data
                return JsonResponse(responses[success], safe=False, status=status.HTTP_201_CREATED)
            else:
                del responses[success]
                return JsonResponse(responses, safe=False, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST', 'PUT'])
    @parser_classes([JSONParser])
    @permission_classes([HasAPIKey])
    # @throttle_classes([HundredPerDayThrottle])
    def json_view(request, format=None):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = APIKey.objects.get_from_key(key)
        if request.method == 'POST':
            if api_key is not None:
                if 'students' not in request.data:
                    return JsonResponse("You did not specify any students for the request.",
                                        safe=False,
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return CreateStudents.return_result(request.data, 'POST')
            else:
                return JsonResponse("No valid credentials were provided", safe=False, status=status.HTTP_401_UNAUTHORIZED)

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
                        if 'normal_gpa' in d:
                            student.normal_gpa = d['normal_gpa']
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
    # @throttle_classes([HundredPerDayThrottle])
    def form_view(request, format=None):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = APIKey.objects.get_from_key(key)
        if request.method == 'POST':
            if api_key != None:
                student = get_object(request.data['email'])
                if student:
                    return JsonResponse("Student with that email already exists", safe=False, status=status.HTTP_409_CONFLICT)
                else:
                    serializer = StudentSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse("No API In Database", safe=False, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            if api_key is not None:
                data = request.data
                student = get_object(data['email'])

                if student:
                    serializer = StudentSerializer(student, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(serializer.data,status=status.HTTP_200_OK)
                    return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse("Student not found.", safe=False, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("No API In Database", safe=False, status=status.HTTP_400_BAD_REQUEST)
