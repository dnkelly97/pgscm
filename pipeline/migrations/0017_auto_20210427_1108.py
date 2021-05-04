# Generated by Django 3.1.5 on 2021-04-27 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_student_submit_demo'),
        ('pipeline', '0016_auto_20210422_0241'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField()),
                ('batch_id', models.IntegerField(blank=True, null=True)),
                ('member_id', models.CharField(blank=True, max_length=100)),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pipeline.stage')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.RemoveField(
            model_name='stage',
            name='students',
        ),
        migrations.AddField(
            model_name='stage',
            name='students',
            field=models.ManyToManyField(through='pipeline.StudentStage', to='student.Student'),
        ),
    ]