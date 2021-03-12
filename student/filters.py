import django_filters
from django.db.models import Q
from django_filters import CharFilter

from .models import Student


def query_combined(queryset, name, value):
    return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value))


class StudentFilter(django_filters.FilterSet):
    name = CharFilter(method=query_combined, label="Search by name/email")

    # first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
    # last_name = CharFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['name',
                  'school_year',
                  'degree',
                  'university',
                  'gpa',
                  'ethnicity',
                  'gender',
                  'country',
                  'us_citizenship',
                  'first_generation',
                  'military']
