# Generated by Django 3.2.6 on 2021-08-30 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vitrek', '0014_auto_20210827_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measures',
            name='point',
        ),
        migrations.RemoveField(
            model_name='measurepoint',
            name='device',
        ),
        migrations.AddField(
            model_name='customer',
            name='number',
            field=models.CharField(default='0', max_length=64),
        ),
        migrations.AddField(
            model_name='customer',
            name='type',
            field=models.CharField(default='0', max_length=256),
        ),
        migrations.AddField(
            model_name='measurepoint',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vitrek.customer'),
        ),
        migrations.AddField(
            model_name='measurepoint',
            name='measures',
            field=models.JSONField(default={'data': []}),
        ),
        migrations.AlterField(
            model_name='measurepoint',
            name='measurePoint',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='Device',
        ),
        migrations.DeleteModel(
            name='Measures',
        ),
    ]
