# Generated by Django 3.0.2 on 2020-03-04 17:32

from django.db import migrations
import streamfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pagine', '0012_auto_20200207_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='upgrade_stream',
            field=streamfield.fields.StreamField(blank=True, default='[]', verbose_name='Aggiornamenti'),
        ),
    ]
