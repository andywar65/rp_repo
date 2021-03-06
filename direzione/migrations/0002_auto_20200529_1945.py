# Generated by Django 3.0.6 on 2020-05-29 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('direzione', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society',
            name='executive',
            field=models.ManyToManyField(related_name='society_executive', to=settings.AUTH_USER_MODEL, verbose_name='Dirigenti'),
        ),
        migrations.AlterField(
            model_name='society',
            name='president',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='society_president', to=settings.AUTH_USER_MODEL, verbose_name='Presidente'),
        ),
        migrations.AlterField(
            model_name='society',
            name='trainers',
            field=models.ManyToManyField(related_name='society_trainers', to=settings.AUTH_USER_MODEL, verbose_name='Istruttori'),
        ),
    ]
