# Generated by Django 3.0.2 on 2020-01-26 22:12

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pagine.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Il titolo dell'articolo", max_length=50, verbose_name='Titolo')),
                ('slug', models.SlugField(editable=False, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
                ('intro', models.CharField(default='Un altro articolo di approfondimento da RP!', max_length=100, verbose_name='Introduzione')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(help_text='Scrivi qualcosa.', verbose_name='Testo')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Autore')),
            ],
            options={
                'verbose_name': 'Articolo',
                'verbose_name_plural': 'Articoli',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Il titolo dell'evento", max_length=50, verbose_name='Titolo')),
                ('slug', models.SlugField(editable=False, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Quando')),
                ('intro', models.CharField(default='Un altro appuntamento con RP!', max_length=100, verbose_name='Introduzione')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(help_text='Scrivi qualcosa.', verbose_name='Lancio')),
                ('chronicle', ckeditor_uploader.fields.RichTextUploadingField(default="Inserisci qui la cronaca dell'evento", verbose_name='Cronaca')),
                ('restricted', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Inserisci qui materiale riservato ai soci', null=True, verbose_name='Area riservata')),
                ('notice', models.CharField(blank=True, choices=[('NOSP', 'Non inviare'), ('SPAM', 'Da inviare'), ('DONE', 'Già inviata')], help_text="Non invia in automatico, per farlo seleziona l'Evento\n            dalla Lista degli Eventi, imposta l'azione 'Invia notifica' e fai\n            clic su 'Vai'.\n            ", max_length=4, null=True, verbose_name='Notifica via email')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventi',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='ImageEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, editable=False, max_length=50, null=True, verbose_name='Nome')),
                ('date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('image', models.ImageField(upload_to=pagine.models.date_directory_path)),
                ('thumb', models.CharField(blank=True, editable=False, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descrizione')),
            ],
            options={
                'verbose_name': 'Immagine',
                'verbose_name_plural': 'Immagini',
            },
        ),
        migrations.CreateModel(
            name='UserUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
                ('image', models.ImageField(blank=True, null=True, upload_to=pagine.models.date_directory_path, verbose_name='Immagine')),
                ('body', models.TextField(help_text='Scrivi qualcosa.', verbose_name='Testo')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_uploads', to='pagine.Event')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_uploads', to='pagine.Blog')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Utente')),
            ],
            options={
                'verbose_name': 'Contributo',
                'verbose_name_plural': 'Contributi',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Il nome del luogo', max_length=50, verbose_name='Titolo')),
                ('slug', models.SlugField(unique=True)),
                ('address', models.CharField(help_text='Via/Piazza, civico, CAP, Città', max_length=200, verbose_name='Indirizzo')),
                ('gmap_link', models.URLField(blank=True, help_text="Dal menu di Google Maps seleziona 'Condividi/link',                    copia il link e incollalo qui", null=True, verbose_name='Link di Google Map')),
                ('gmap_embed', models.TextField(blank=True, help_text="Dal menu di Google Maps seleziona 'Condividi/incorpora',                    copia il link e incollalo qui", max_length=500, null=True, verbose_name='Incorpora Google Map')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Descrizione')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Sito internet')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telefono/i')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagine.ImageEntry', verbose_name='Immagine')),
            ],
            options={
                'verbose_name': 'Luogo',
                'verbose_name_plural': 'Luoghi',
            },
        ),
        migrations.CreateModel(
            name='EventUpgrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Il titolo dell'aggiornamento", max_length=50, verbose_name='Titolo')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
                ('body', models.TextField(help_text='Scrivi qualcosa.', verbose_name='Aggiornamento')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_upgrades', to='pagine.Event')),
            ],
            options={
                'verbose_name': 'Aggiornamento',
                'verbose_name_plural': 'Aggiornamenti',
                'ordering': ('-date',),
            },
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagine.ImageEntry', verbose_name='Immagine'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagine.Location', verbose_name='Dove'),
        ),
        migrations.AddField(
            model_name='event',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Responsabile'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Lista di categorie separate da virgole', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Categorie'),
        ),
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagine.ImageEntry', verbose_name='Immagine'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Lista di categorie separate da virgole', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Categorie'),
        ),
    ]
