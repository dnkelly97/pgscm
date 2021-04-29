import django_filters
from django.db.models import Q
from django_filters import CharFilter, NumberFilter

from .models import Student


def query_degree(queryset, name, value):
    return queryset.filter(Q(degree__icontains=value))


def query_uni(queryset, name, value):
    return queryset.filter(Q(university__icontains=value))


def query_interest(queryset, name, value):
    return queryset.filter(Q(research_interests__icontains=value))


def query_combined(queryset, name, value):
    return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value))


class StudentFilter(django_filters.FilterSet):
    name = CharFilter(method=query_combined, label="Search by name/email")
    research_interests = CharFilter(method=query_interest, label="Research of Interest")
    university = CharFilter(method=query_uni, label="University")
    degree = CharFilter(method=query_degree, label="Degree")
    gpa_start = NumberFilter(field_name="normal_gpa", lookup_expr='gte')
    gpa_end = NumberFilter(field_name="normal_gpa", lookup_expr='lte')

    class Meta:
        model = Student
        fields = ['name',
                  'school_year',
                  'degree',
                  'university',
                  'research_interests',
                  'gpa_start',
                  'gpa_end',
                  'ethnicity',
                  'gender',
                  'country',
                  'us_citizenship',
                  'first_generation',
                  'military']