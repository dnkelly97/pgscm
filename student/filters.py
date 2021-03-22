import django_filters
from django.db.models import Q
from django_filters import CharFilter

from .models import Student


def query_interest(queryset, name, value):
    return queryset.filter(Q(research_interests__icontains=value))


def query_combined(queryset, name, value):
    return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value))


class StudentFilter(django_filters.FilterSet):
    name = CharFilter(method=query_combined, label="Search by name/email")
    research_interests = CharFilter(method=query_interest, label="Research of Interest")

    class Meta:
        model = Student
        fields = ['name',
                  'school_year',
                  'degree',
                  'university',
                  'research_interests',
                  'gpa',
                  'ethnicity',
                  'gender',
                  'country',
                  'us_citizenship',
                  'first_generation',
                  'military']
