# Generated by Django 3.1.5 on 2021-04-07 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0013_pipeline_sources'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='sources',
            field=models.ManyToManyField(blank=True, null=True, to='pipeline.SavedQuery'),
        ),
    ]
