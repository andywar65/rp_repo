import re
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.utils.timezone import now
from django.utils.html import format_html, strip_tags

from filebrowser.fields import FileBrowseField
from taggit.managers import TaggableManager
from streamfield.fields import StreamField

from streamblocks.models import (IndexedParagraph, CaptionedImage, Gallery,
    LandscapeGallery, DownloadableFile, LinkableList, BoxedText, EventUpgrade)
from users.models import User, Profile
from project.utils import generate_unique_slug

from .choices import *

class Location(models.Model):
    fb_image = FileBrowseField("Immagine", max_length=200,
        directory="locations/", extensions=[".jpg", ".png", ".jpeg", ".gif",
        ".tif", ".tiff"], null=True, blank=True)
    title = models.CharField('Titolo',
        help_text='Il nome del luogo',
        max_length = 50)
    slug = models.SlugField(max_length=50, unique=True)
    address = models.CharField('Indirizzo', max_length = 200,
        help_text = 'Via/Piazza, civico, CAP, Città',)
    gmap_link = models.URLField('Link di Google Map',
        blank= True, null=True,
        help_text="Dal menu di Google Maps seleziona 'Condividi/link', \
                   copia il link e incollalo qui",
    )
    gmap_embed = models.TextField('Incorpora Google Map',
        blank= True, null=True, max_length=500,
        help_text="Dal menu di Google Maps seleziona 'Condividi/incorpora', \
                   copia il link e incollalo qui",
    )
    body = models.TextField('Descrizione', blank= True, null=True,)
    website = models.URLField('Sito internet',
        blank= True, null=True, )
    email = models.EmailField(blank = True, null = True,
        verbose_name = 'Email',)
    phone = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Telefono/i',)

    def save(self, *args, **kwargs):
        if not self.gmap_embed.startswith('http'):
            # thanks to geeksforgeeks.com! findall returns a list
            list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.gmap_embed)
            if list:
                self.gmap_embed = list[0]
        if not self.slug:  # create
            self.slug = generate_unique_slug(Location, self.title)
        super(Location, self).save(*args, **kwargs)

    def get_gmap_link(self):
        if self.gmap_link:
            link = format_html('<a href="{}" class="btn" target="_blank">Mappa</a>',
                self.gmap_link)
        else:
            link = '-'
        return link
    get_gmap_link.short_description = 'Link di Google Maps'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Luogo'
        verbose_name_plural = 'Luoghi'
        ordering = ('id', )

#def update_indexed_paragraphs(stream_list, type, id):
    #for block in stream_list:
        #if block['model_name'] == 'IndexedParagraph':
            #par = IndexedParagraph.objects.get(id = block['id'])
            #par.parent_type = type
            #par.parent_id = id
            #par.save()

class Event(models.Model):
    fb_image = FileBrowseField("Immagine", max_length=200, directory="events/",
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True, blank=True)
    carousel = StreamField(model_list=[ LandscapeGallery, ],
        null=True, blank=True, verbose_name="Galleria",
        help_text="Una sola galleria, per favore, larghezza minima immagini 2048px")
    title = models.CharField('Titolo',
        help_text="Il titolo dell'evento",
        max_length = 50)
    slug = models.SlugField(max_length=50, editable=False, null=True)
    date = models.DateTimeField('Quando', default = now)
    last_updated = models.DateTimeField(editable=False, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
        null = True, verbose_name = 'Dove', )
    intro = models.CharField('Introduzione',
        default = 'Un altro appuntamento con RP!', max_length = 100)
    stream = StreamField(model_list=[ IndexedParagraph, CaptionedImage,
        Gallery, DownloadableFile, LinkableList, BoxedText, ],
        verbose_name="Lancio")
    upgrade_stream = StreamField(model_list=[ EventUpgrade, IndexedParagraph,
        DownloadableFile, ],
        verbose_name="Aggiornamenti")
    chron_stream = StreamField(model_list=[ IndexedParagraph, CaptionedImage,
        Gallery, DownloadableFile, LinkableList, BoxedText],
        verbose_name="Cronaca")
    restr_stream = StreamField(model_list=[ IndexedParagraph, CaptionedImage,
        Gallery, DownloadableFile, LinkableList, BoxedText],
        verbose_name="Area riservata",
        help_text="Inserisci qui materiale riservato ai soci",)
    stream_search = models.TextField(editable=False, null=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Responsabile')
    tags = TaggableManager(verbose_name="Categorie",
        help_text="Lista di categorie separate da virgole",
        through=None, blank=True)
    notice = models.CharField(max_length = 4, choices = NOTICE,
        blank = True, null = True, verbose_name = 'Notifica via email',
        help_text = """Invia notifica in automatico selezionando
            'Invia notifica' e salvando l'articolo.
            """)

    def get_badge_color(self):
        if self.date.date() > datetime.today().date():
            return 'success'
        elif self.date.date() < datetime.today().date():
            return 'secondary'
        else:
            return 'warning'

    def get_image(self):
        gallery_list = self.carousel.from_json()
        if gallery_list:
            gallery = gallery_list[0]
            image = LandscapeGallery.objects.filter( id__in = gallery['id'] ).first()
            return image.fb_image
        elif self.location.fb_image:
            return self.location.fb_image
        return

    def get_tags(self):
        return list(self.tags.names())

    #def get_upgrades(self):
        #return EventUpgrade.objects.filter(event_id=self.id)

    def get_chronicle(self):
        if self.date.date() < datetime.today().date():
            return True
        return False

    def get_uploads(self):
        return UserUpload.objects.filter(event_id=self.id)

    def get_path(self):
        return '/calendario/' + self.date.strftime("%Y/%m/%d") + '/' + self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Event, self.title)
        self.last_updated = now()
        self.stream_search = strip_tags(self.stream.render)
        self.stream_search += strip_tags(self.upgrade_stream.render)
        self.stream_search += strip_tags(self.chron_stream.render)
        self.stream_search += strip_tags(self.restr_stream.render)
        if self.notice == 'SPAM':
            message = self.title + '\n'
            message += self.intro + '\n'
            url = settings.BASE_URL + self.get_path()
            message += 'Fai click su questo link per leggerlo: ' + url + '\n'
            recipients = User.objects.filter( is_active = True, )
            #inactive users may not have profile
            recipients = recipients.filter( profile__yes_spam = True, )
            mailto = []
            for recipient in recipients:
                mailto.append(recipient.email)
            subject = f'Nuovo evento su {settings.WEBSITE_NAME}'
            email = EmailMessage(subject, message, settings.SERVER_EMAIL,
                mailto)
            email.send()
            self.notice = 'DONE'
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventi'
        ordering = ('-date', )

#class EventUpgrade(models.Model):
    #event = models.ForeignKey(Event, on_delete = models.CASCADE,
        #null = True, related_name='event_upgrades')
    #title = models.CharField('Titolo',
        #help_text="Il titolo dell'aggiornamento",
        #max_length = 50)
    #date = models.DateTimeField('Data', default = now)
    #body = models.TextField('Aggiornamento',
        #help_text = "Accetta tag HTML.", )

    #def __str__(self):
        #return self.title

    #class Meta:
        #verbose_name = 'Aggiornamento'
        #verbose_name_plural = 'Aggiornamenti'
        #ordering = ('-date', )
