# Generated by Django 3.1.1 on 2020-11-04 18:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0012_auto_20201029_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 18, 25, 44, 946396, tzinfo=utc)),
        ),
    ]
