# Generated by Django 3.2.6 on 2021-08-18 19:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vitrek', '0006_alter_measuressettings_measures_delay_seconds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicemeasures',
            name='Process_Date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
