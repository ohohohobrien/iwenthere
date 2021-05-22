# Generated by Django 3.1.7 on 2021-05-08 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0009_auto_20210503_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='long',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='small_1',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='small_2',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='starting_location',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
