from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import JSONField

from users.models import User
from cronache.models import Event, Location
from project.utils import generate_unique_slug

from .choices import *

class Race(models.Model):
    title = models.CharField('Nome', help_text="Il nome della gara",
        max_length = 50)
    slug = models.SlugField(max_length=50, editable=False, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Evento',
        related_name = 'event_race')
    date = models.DateField('Data', blank= True, null=True,
        help_text="In mancanza di Evento", )
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
        blank= True, null=True, verbose_name = 'Luogo',
        help_text="In mancanza di Evento", )
    type = models.CharField('Tipo', choices = TYPE, max_length = 4,
        blank= True, null=True, )
    description = models.CharField('Descrizione', blank= True, null=True,
        max_length = 500)

    def get_date(self):
        if self.event:
            return self.event.date.date()
        return self.date
    get_date.short_description = 'Data'

    def get_edition(self):
        date = self.get_date()
        year = date.year
        month = date.month
        if month >= 11:
            return str(year) + '-' + str(year+1)
        else:
            return str(year-1) + '-' + str(year)
    get_edition.short_description = 'Edizione'

    def get_path(self):
        return '/criterium/' + self.get_edition() + '/' + self.slug

    def get_location(self):
        if self.event:
            return self.event.location
        return self.location
    get_location.short_description = 'Luogo'

    def save(self, *args, **kwargs):
        if not self.slug:  # create
            self.slug = generate_unique_slug(Race, self.title)
        if not self.date:
            temp = self.event.date
            #conditional added for test to work
            if isinstance(temp, str):
                temp = temp.split(' ')[0]
                self.date = datetime.strptime(temp, '%Y-%m-%d')
            else:
                self.date = temp.date()
        super(Race, self).save(*args, **kwargs)
        RaceCache.objects.get_or_create(race_id = self.id)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Gara'
        verbose_name_plural = 'Gare'
        ordering = ('-date', )

class RaceCache(models.Model):
    race= models.OneToOneField(Race, on_delete=models.CASCADE,
        primary_key=True)
    cache = JSONField(null=True)

class AthleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('user__last_name',
            'user__first_name')

class Athlete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        verbose_name = 'Iscritto', null = True, )
    race = models.ForeignKey(Race, on_delete=models.CASCADE,
        editable = False, null = True, )
    points = models.IntegerField('Punti')
    placement = models.IntegerField('Piazzamento assoluto', blank = True,
        null = True, )
    time = models.TimeField('Tempo', blank = True, null = True, )

    objects = AthleteManager()

    def __str__(self):
        return self.user.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atleti/e'
