# Generated by Django 3.2.5 on 2021-07-15 00:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_auto_20210714_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 15, 9, 1, 37, 787500)),
        ),
    ]
