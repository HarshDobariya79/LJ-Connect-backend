# Generated by Django 4.1.10 on 2023-08-26 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0016_department_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffdetail',
            name='admin',
            field=models.BooleanField(default=False, help_text='Is the staff admin?', verbose_name='admin'),
        ),
    ]
