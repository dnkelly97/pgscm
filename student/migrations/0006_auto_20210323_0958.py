# Generated by Django 3.1.5 on 2021-03-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_student_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_profile.png', null=True, upload_to=''),
        ),
    ]