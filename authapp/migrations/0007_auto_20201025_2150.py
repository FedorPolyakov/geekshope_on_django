# Generated by Django 3.1.1 on 2020-10-25 18:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20201024_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 27, 18, 50, 0, 141522, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='about_me',
            field=models.TextField(blank=True, verbose_name='Обо мне'),
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'М'), ('F', 'Ж')], max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='tagline',
            field=models.CharField(blank=True, max_length=128, verbose_name='тэги'),
        ),
    ]
