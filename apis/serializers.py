from rest_framework import serializers
from student.models import Student
from django_countries.serializers import CountryFieldMixin


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
                  'gpa',
                  'ethnicity',
                  'gender',
                  'country',
                  'us_citizenship',
                  'first_generation',
                  'military',
                  'resume',
                  # 'transcript',
                  # 'profile_image',
                  )
