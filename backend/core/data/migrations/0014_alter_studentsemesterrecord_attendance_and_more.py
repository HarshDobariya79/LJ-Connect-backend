# Generated by Django 4.1.10 on 2023-07-31 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_attendance_create_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsemesterrecord',
            name='attendance',
            field=models.ManyToManyField(blank=True, to='data.attendance', verbose_name='Attendance'),
        ),
        migrations.AlterField(
            model_name='studentsemesterrecord',
            name='test_result',
            field=models.ManyToManyField(blank=True, to='data.testresult', verbose_name='Test Result'),
        ),
    ]
