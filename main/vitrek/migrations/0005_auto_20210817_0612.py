# Generated by Django 3.2.6 on 2021-08-17 06:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vitrek', '0004_auto_20210817_0609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicedata',
            name='Process_Date',
        ),
        migrations.AddField(
            model_name='devicemeasures',
            name='Process_Date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
