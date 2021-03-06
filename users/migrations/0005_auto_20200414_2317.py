# Generated by Django 3.0.5 on 2020-04-14 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_sector'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, help_text='Via/Piazza, civico, CAP, Città', max_length=100, null=True, verbose_name='Indirizzo'),
        ),
        migrations.AddField(
            model_name='profile',
            name='email_2',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Seconda email'),
        ),
        migrations.AddField(
            model_name='profile',
            name='fiscal_code',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Codice fiscale'),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Telefono/i'),
        ),
    ]
