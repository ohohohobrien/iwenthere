# Generated by Django 3.1.7 on 2021-05-03 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_auto_20210420_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='cover',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
    ]
