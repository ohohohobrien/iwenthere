# Generated by Django 3.1.7 on 2021-05-03 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0008_auto_20210503_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='cover',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
