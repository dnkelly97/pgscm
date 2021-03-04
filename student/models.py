from django.db import models
from django_countries.fields import CountryField

class Student(models.Model):
    #Initial criteria
    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    #School Related
    class YearInSchool(models.TextChoices):
        FRESHMAN = 'FR', _('Freshman')
        SOPHOMORE = 'SO', _('Sophomore')
        JUNIOR = 'JR', _('Junior')
        SENIOR = 'SR', _('Senior')
        GRADUATE = 'GR', _('Graduate')

    school_year = models.CharField(
        max_length=2,
        choices=YearInSchool.choices
    )

    research_interests = models.ArrayField(
        models.CharField(max_length=55, blank=True)
    )

    degree = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    gpa = models.FloatField(default=0)

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

    ethnicity = models.CharField(
        max_length=1,
        choices=Ethnicity.choices
    )

    # School Related
    class Gender(models.TextChoices):
        FEMALE = 'F', _('Female')
        MALE = 'M', _('Male')
        NONBINARY = 'N', _('Non-Binary/Non-Conforming')
        OTHER = 'O', _('Other')
        QUEER = 'Q', _('Queer')
        TRANSGENDER = 'T', _('Transgender')

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices
    )
    country = CountryField(blank_label='(select country)')
    us_citizenship = models.BooleanField(null=True)
    first_generation = models.BooleanField(null=True)
    military = models.BooleanField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
