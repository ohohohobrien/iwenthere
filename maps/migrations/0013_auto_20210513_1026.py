# Generated by Django 3.1.7 on 2021-05-13 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0012_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='FULL_NAME_ND',
            new_name='STATE_NAME',
        ),
    ]
