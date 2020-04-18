# Generated by Django 3.0.5 on 2020-04-18 21:04

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile_is_trusted'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mc_expiry',
            field=models.DateField(blank=True, null=True, verbose_name='Scadenza CM/CMA'),
        ),
        migrations.AddField(
            model_name='profile',
            name='mc_state',
            field=models.CharField(blank=True, choices=[('0-NF', 'Manca il file'), ('1-VF', 'Verifica file'), ('2-RE', 'Regolare'), ('6-IS', 'In scadenza'), ('3-SV', 'Scaduto, da verificare'), ('4-SI', 'Scaduto, inviare notifica'), ('5-NI', 'Scaduto, notifica inviata')], max_length=4, null=True, verbose_name='Stato del CM/CMA'),
        ),
        migrations.AddField(
            model_name='profile',
            name='membership',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Tessera'),
        ),
        migrations.AddField(
            model_name='profile',
            name='settled',
            field=models.CharField(blank=True, choices=[('VI', 'Verifica importo totale'), ('YES', 'A posto'), ('NO', 'No!')], max_length=4, null=True, verbose_name='In regola?'),
        ),
        migrations.AddField(
            model_name='profile',
            name='total_amount',
            field=models.FloatField(default=0.0, verbose_name='Importo totale'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_trusted',
            field=models.BooleanField(default=False, verbose_name='Di fiducia'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to=users.models.user_directory_path, verbose_name='Allegato'),
        ),
    ]
