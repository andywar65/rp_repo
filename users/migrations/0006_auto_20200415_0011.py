# Generated by Django 3.0.5 on 2020-04-14 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200414_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Data di nascita'),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('F', 'Femmina'), ('M', 'Maschio')], max_length=1, null=True, verbose_name='Sesso'),
        ),
        migrations.AddField(
            model_name='profile',
            name='nationality',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nazionalità'),
        ),
        migrations.AddField(
            model_name='profile',
            name='place_of_birth',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Luogo di nascita'),
        ),
    ]
