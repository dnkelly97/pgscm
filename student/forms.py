from django.forms import ModelForm
from student.models import Student
from django import forms

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
                  'military',
                  'resume',
                  'transcript',
                  'profile_image']


class EmailForm(forms.Form):
    from_email = forms.EmailField(required=True)
