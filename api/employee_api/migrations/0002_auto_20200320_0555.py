# Generated by Django 3.0.4 on 2020-03-20 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='employee',
            new_name='employee_id',
        ),
    ]
