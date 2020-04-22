# Generated by Django 3.0.2 on 2020-02-07 13:11

from django.db import migrations
import streamfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pagine', '0008_auto_20200207_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='body',
        ),
        migrations.AddField(
            model_name='event',
            name='stream',
            field=streamfield.fields.StreamField(blank=True, default='[]', verbose_name='Lancio'),
        ),
        migrations.AlterField(
            model_name='event',
            name='chronicle',
            field=streamfield.fields.StreamField(blank=True, default='[]', verbose_name='Cronaca'),
        ),
        migrations.AlterField(
            model_name='event',
            name='restricted',
            field=streamfield.fields.StreamField(blank=True, default='[]', help_text='Inserisci qui materiale riservato ai soci', verbose_name='Area riservata'),
        ),
    ]
