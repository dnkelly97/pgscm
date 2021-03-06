from rest_framework import serializers
from student.models import Student
from django_countries.serializers import CountryFieldMixin


class JSONStudentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

class StudentSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('email',
                  'first_name',
                  'last_name',
                  'school_year',
                  'research_interests',
                  'degree',
                  'university',
                  'normal_gpa',
                  'ethnicity',
                  'gender',
                  'country',
                  'us_citizenship',
                  'first_generation',
                  'military',
                  'resume',
                  'transcript',
                  'profile_image',
                  )
