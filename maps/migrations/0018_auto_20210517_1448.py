# Generated by Django 3.1.7 on 2021-05-17 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0017_auto_20210517_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='distance',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]