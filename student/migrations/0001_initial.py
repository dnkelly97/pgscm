
# Generated by Django 3.1.5 on 2021-03-08 21:08


import django.contrib.postgres.fields
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('school_year', models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate'), ('UN', 'Unknown')], default='UN', max_length=2)),
                ('research_interests', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=55), blank=True, null=True, size=None)),
                ('degree', models.CharField(blank=True, max_length=255)),
                ('university', models.CharField(blank=True, max_length=255)),
                ('gpa', models.FloatField(blank=True, null=True)),
                ('ethnicity', models.CharField(choices=[('A', 'Asian American'), ('B', 'Black / African American'), ('H', 'Hispanic / Latinx'), ('M', 'Multiracial'), ('N', 'Native American / Alaskan Native'), ('O', 'Prefer Not To Say'), ('W', 'White / Non Hispanic'), ('U', 'Unknown')], default='U', max_length=1)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('N', 'Non-Binary/Non-Conforming'), ('O', 'Other'), ('Q', 'Queer'), ('T', 'Transgender'), ('U', 'Unknown')], default='U', max_length=1)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('us_citizenship', models.BooleanField(blank=True, null=True)),
                ('first_generation', models.BooleanField(blank=True, null=True)),
                ('military', models.BooleanField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]