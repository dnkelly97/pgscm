# Generated by Django 3.1.5 on 2021-04-22 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0015_auto_20210408_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='placeholders',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='stage',
            name='template_url',
            field=models.CharField(blank=True, max_length=55),
        ),
    ]
