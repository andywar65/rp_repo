# Generated by Django 3.0.4 on 2020-03-22 16:49

from django.db import migrations, models
import streamfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carousel', streamfield.fields.StreamField(blank=True, default='[]', help_text='Una sola galleria, per favore, larghezza minima immagini 2048px', null=True, verbose_name='Galleria orizzontale')),
                ('intro', models.CharField(blank=True, help_text='Il sito in due parole', max_length=100, null=True, verbose_name='Sottotitolo')),
                ('action', streamfield.fields.StreamField(blank=True, default='[]', help_text='Link a pagine sponsorizzate.', null=True, verbose_name='Pulsanti di azione')),
            ],
            options={
                'verbose_name': 'Home Page',
            },
        ),
        migrations.CreateModel(
            name='TreePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=50, verbose_name='Titolo')),
                ('slug', models.SlugField(blank=True, help_text="Titolo come appare nell'indirizzo della pagina,\n            solo lettere minuscole e senza spazi", null=True, unique=True, verbose_name='Slug')),
                ('intro', models.TextField(blank=True, max_length=200, null=True, verbose_name='Introduzione')),
                ('stream', streamfield.fields.StreamField(blank=True, default='[]', verbose_name='Testo')),
                ('summary', models.BooleanField(default=True, verbose_name='Mostra sommario')),
                ('last_updated', models.DateTimeField(editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Pagina ad albero',
                'verbose_name_plural': 'Pagine ad albero',
            },
        ),
    ]
