# Generated by Django 3.1.5 on 2021-05-02 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0018_merge_20210429_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='subject',
            field=models.CharField(max_length=100, null=True),
        ),
    ]