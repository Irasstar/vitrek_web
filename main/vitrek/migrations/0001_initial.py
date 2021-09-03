# Generated by Django 3.2.6 on 2021-08-16 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentMeasures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acv', models.FloatField()),
                ('dcv', models.FloatField()),
                ('frequency', models.FloatField()),
                ('Pk_pk', models.FloatField()),
                ('Crf', models.FloatField()),
                ('Date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='DeviceMeasures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acv', models.FloatField()),
                ('dcv', models.FloatField()),
                ('frequency', models.FloatField()),
                ('Pk_pk', models.FloatField()),
                ('Crf', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DeviceData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Device_Number', models.CharField(max_length=64)),
                ('Device_Name', models.CharField(max_length=256)),
                ('Additional_Info', models.CharField(max_length=1024)),
                ('Process_Date', models.DateTimeField()),
                ('Measures', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vitrek.devicemeasures')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer_name', models.CharField(max_length=1024)),
                ('Customer_code', models.IntegerField()),
                ('Customer_address', models.CharField(max_length=1024)),
                ('Devices', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vitrek.devicedata')),
            ],
        ),
    ]