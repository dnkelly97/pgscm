from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.contrib.postgres.fields import ArrayField

class Student(models.Model):
    #Initial criteria
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    #School Related
    class YearInSchool(models.TextChoices):
        FRESHMAN = 'FR', _('Freshman')
        SOPHOMORE = 'SO', _('Sophomore')
        JUNIOR = 'JR', _('Junior')
        SENIOR = 'SR', _('Senior')
        GRADUATE = 'GR', _('Graduate')
        UNKNOWN = 'UN', _('Unknown')

    school_year = models.CharField(
        max_length=2,
        choices=YearInSchool.choices,
        default=YearInSchool.UNKNOWN
    )

    research_interests = ArrayField(
        models.CharField(max_length=55),blank=True,null=True
    )

    degree = models.CharField(max_length=255,blank=True)
    university = models.CharField(max_length=255,blank=True)
    gpa = models.FloatField(blank=True,null=True)

    #demographic info
    #https://usg.uiowa.edu/assets/Documents/Reports-Guides-and-Plans/UISG-2018-2019-Fall-Demographics-Report.pdf
    class Ethnicity(models.TextChoices):
        ASIAN = 'A', _('Asian American')
        BLACK = 'B', _('Black / African American')
        HISPANIC = 'H', _('Hispanic / Latinx')
        MULTI = 'M', _('Multiracial')
        NATIVE = 'N', _('Native American / Alaskan Native')
        OTHER = 'O', _('Prefer Not To Say')
        WHITE = 'W', _('White / Non Hispanic')
        UNKNOWN = 'U', _('Unknown')

    ethnicity = models.CharField(
        max_length=1,
        choices=Ethnicity.choices,
        default=Ethnicity.UNKNOWN
    )

    # School Related
    class Gender(models.TextChoices):
        FEMALE = 'F', _('Female')
        MALE = 'M', _('Male')
        NONBINARY = 'N', _('Non-Binary/Non-Conforming')
        OTHER = 'O', _('Other')
        QUEER = 'Q', _('Queer')
        TRANSGENDER = 'T', _('Transgender')
        UNKNOWN = 'U', _('Unknown')

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.UNKNOWN
    )

    country = CountryField(blank_label='(select country)',null=True,blank=True)
    us_citizenship = models.BooleanField(blank=True,null=True)
    first_generation = models.BooleanField(blank=True,null=True)
    military = models.BooleanField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
