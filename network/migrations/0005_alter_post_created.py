# Generated by Django 3.2.5 on 2021-07-09 22:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_post_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 10, 7, 13, 4, 919979)),
        ),
    ]
