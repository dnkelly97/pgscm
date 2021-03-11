from django.forms import ModelForm
from student.models import Student

class CreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['email',
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
                  'military']