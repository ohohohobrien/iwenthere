# Generated by Django 3.1.7 on 2021-05-14 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0014_country'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='City',
            new_name='State',
        ),
    ]