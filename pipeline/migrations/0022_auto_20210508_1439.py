# Generated by Django 3.1.5 on 2021-05-08 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0021_merge_20210503_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='template_url',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]