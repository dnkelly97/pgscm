# Generated by Django 3.1.5 on 2021-04-27 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0016_auto_20210422_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]