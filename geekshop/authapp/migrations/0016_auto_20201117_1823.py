# Generated by Django 3.1.1 on 2020-11-17 15:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0015_auto_20201116_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 19, 15, 23, 57, 260555, tzinfo=utc)),
        ),
    ]
