# Generated by Django 4.1.10 on 2023-07-27 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_attendance_lecture_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='lecture_no',
            field=models.CharField(max_length=1, verbose_name='Lecture No.'),
        ),
    ]
