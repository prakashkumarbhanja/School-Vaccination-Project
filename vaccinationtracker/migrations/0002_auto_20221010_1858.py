# Generated by Django 3.2.16 on 2022-10-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinationtracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaccinationDrive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('no_of_slots', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(default='Bhubaneswar, Odisha', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='city',
            field=models.CharField(default='Bhubaneswar', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='name_of_vaccination',
            field=models.CharField(default='covaxin', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='state',
            field=models.CharField(default='Odish', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='vaccination_date',
            field=models.CharField(default='08-10-2022', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='vaccination_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='zip',
            field=models.IntegerField(default=751023),
            preserve_default=False,
        ),
    ]
