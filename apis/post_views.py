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

def json_data_formatter(student,status_code, errors=None):
    if errors:
        return {
            "code": status_code,
            "errors": errors,
            "student": student
        }
    else:
        return {
            "code": status_code,
            "student": student
        }

class CreateStudents(APIView):

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
                    bad_request = 400
                    success = 201
                    conflict = 409
                    data = request.data
                    valid = []
                    invalid = []

                    if 'save_valid' in data:
                        save_valid = data['save_valid']
                    else:
                        save_valid = False

                    for student in data['students']:
                        json_serializer = JSONStudentSerializer(data=student)
                        if json_serializer.is_valid():
                            student_serializer = StudentSerializer(data=student)
                            if student_serializer.is_valid():
                                if save_valid:
                                    student_serializer.save()
                                valid.append(json_data_formatter(student_serializer.data,success))
                            else:
                                invalid.append(
                                    json_data_formatter(student_serializer.data,conflict, student_serializer.errors))
                        else:
                            invalid.append(
                                json_data_formatter(json_serializer.data, bad_request, json_serializer.errors))

                    if save_valid:
                        if not invalid:
                            return JsonResponse(valid, safe=False, status=status.HTTP_201_CREATED)
                        else:
                            return JsonResponse(valid+invalid, safe=False, status=status.HTTP_207_MULTI_STATUS)
                    else:
                        if not invalid:
                            data = [ student['student'] for student in valid ]
                            serializer = StudentSerializer(data=data, many=True)
                            serializer.is_valid()
                            serializer.save()
                            return JsonResponse(valid, safe=False, status=status.HTTP_201_CREATED)
                        else:
                            return JsonResponse(invalid, safe=False, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse("No valid credentials were provided", safe=False, status=status.HTTP_401_UNAUTHORIZED)

        elif request.method == 'PUT':
            if api_key is not None:
                if 'students' not in request.data:
                    return JsonResponse("You did not specify any students for the request.",
                                        safe=False,
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    bad_request = 400
                    success = 200
                    not_found = 404
                    data = request.data
                    valid = []
                    invalid = []

                    if 'save_valid' in data:
                        save_valid = data['save_valid']
                    else:
                        save_valid = False

                    for student in data['students']:
                        json_serializer = JSONStudentSerializer(data=student)
                        if json_serializer.is_valid():
                            update_student = get_object(student['email'])
                            if update_student:
                                student_serializer = StudentSerializer(update_student,data=student)
                                if student_serializer.is_valid():
                                    if save_valid:
                                        student_serializer.save()
                                    valid.append(json_data_formatter(student_serializer.data, success))
                                else:
                                    invalid.append(json_data_formatter(json_serializer.data, bad_request, json_serializer.errors))
                            else:
                                invalid.append(
                                    json_data_formatter(student, not_found, {"email": ["student with this email does not exist."]}))
                        else:
                            invalid.append(
                                json_data_formatter(json_serializer.data, bad_request, json_serializer.errors))

                    if save_valid:
                        if not invalid:
                            return JsonResponse(valid, safe=False, status=status.HTTP_200_OK)
                        else:
                            return JsonResponse(valid + invalid, safe=False, status=status.HTTP_207_MULTI_STATUS)
                    else:
                        if not invalid:
                            data = [student['student'] for student in valid]
                            for person in data:
                                update_student = get_object(person['email'])
                                serializer = StudentSerializer(update_student, data=person)
                                serializer.is_valid()
                                serializer.save()
                            return JsonResponse(valid, safe=False, status=status.HTTP_200_OK)
                        else:
                            return JsonResponse(invalid, safe=False, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse("No valid credentials were provided", safe=False,
                                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse("Method not allowed.", safe=False,
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
