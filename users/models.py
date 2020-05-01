import os
from datetime import date, timedelta
from PIL import Image

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from django.utils.html import format_html

from filebrowser.fields import FileBrowseField
from filebrowser.base import FileObject
from .choices import *
from .validators import validate_codice_fiscale

class User(AbstractUser):

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.username
    get_full_name.short_description = 'Nome'

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username

    def get_children(self):
        return User.objects.filter(profile__parent_id = self.id)

    def is_adult(self):
        if not self.profile.date_of_birth:
            return False
        age = ( date.today() - self.profile.date_of_birth ).days
        if age >= 18*365:
            return True
        return False

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_active:
            try:
                memb = Profile.objects.get(user_id = self.id)
                return
            except:
                memb = Profile.objects.create(user = self)
                memb.save()
                return

    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'

class CourseSchedule(models.Model):
    full = models.CharField(max_length = 32, verbose_name = 'Giorno e ora',)
    abbrev = models.CharField(max_length = 8, verbose_name = 'Abbreviazione',)

    def __str__(self):
        return self.full

    class Meta:
        verbose_name = 'Orario'
        verbose_name_plural = 'Orari'

def user_directory_path(instance, filename):
    return 'uploads/users/{0}/{1}'.format(instance.user.username, filename)

def mc_state_email(mailto, name, state):
    message = f"""Buongiorno \n
        Il CM/CMA di {name} risulta {state}. \n
        Si prega di provvedere al più presto. Grazie. \n
        Lo staff di RP"""
    subject = 'Verifica CM/CMA'
    email = EmailMessage(subject, message, settings.SERVER_EMAIL,
        mailto)
    email.send()

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True, editable=False)
    parent = models.ForeignKey(User, on_delete = models.SET_NULL,
        blank = True, null = True, related_name = 'profile_parent',
        verbose_name = 'Genitore')
    avatar = models.ImageField(blank = True, null=True,
        upload_to = user_directory_path)
    bio = models.TextField("Breve biografia", null=True, blank=True)
    yes_spam = models.BooleanField(default = False,
        verbose_name = 'Mailing list',
        help_text = 'Vuoi ricevere notifiche sugli eventi?',)
    sector = models.CharField(max_length = 4, choices = SECTOR,
        default = '0-NO', verbose_name = 'Corri con noi?')
    gender = models.CharField(max_length = 1, choices = GENDER,
        null=True, verbose_name = 'Sesso', )
    date_of_birth = models.DateField( null=True,
        verbose_name = 'Data di nascita',)
    place_of_birth = models.CharField(max_length = 50,
        null = True, verbose_name = 'Luogo di nascita',)
    nationality = models.CharField(max_length = 50,
        null = True, verbose_name = 'Nazionalità',)
    fiscal_code = models.CharField(max_length = 16,
        null = True, verbose_name = 'Codice fiscale',
        validators=[validate_codice_fiscale])
    address = models.CharField(max_length = 100,
        null = True, verbose_name = 'Indirizzo',
        help_text = 'Via/Piazza, civico, CAP, Città',)
    phone = models.CharField(max_length = 50,
        null = True, verbose_name = 'Telefono/i',)
    email_2 = models.EmailField(blank = True, null = True,
        verbose_name = 'Seconda email',)
    course = models.ManyToManyField(CourseSchedule,
        blank = True, verbose_name = 'Orari scelti', )
    course_alt = models.CharField(max_length = 100,
        blank = True, null = True, verbose_name = 'Altro orario',
        help_text = "Solo se si è selezionato 'Altro'")
    course_membership = models.CharField(max_length = 4, choices = COURSE,
        null = True, verbose_name = 'Federazione / Ente sportivo',
        )
    no_course_membership = models.CharField(max_length = 4, choices = NO_COURSE,
        null = True, verbose_name = 'Federazione / Ente sportivo',
        )
    sign_up = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Richiesta di tesseramento',
        )
    privacy = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Privacy',
        )
    med_cert = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Certificato medico',
        )
    is_trusted = models.BooleanField(default = False,
        verbose_name = 'Di fiducia',)
    membership = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Tessera',)
    mc_expiry = models.DateField( blank=True, null=True,
        verbose_name = 'Scadenza CM/CMA',)
    mc_state = models.CharField(max_length = 4, choices = MC_STATE,
        verbose_name = 'Stato del CM/CMA',
        blank = True, null = True, )
    total_amount = models.FloatField( default = 0.00,
        verbose_name = 'Importo totale')
    settled = models.CharField(max_length = 4, choices = SETTLED,
        blank=True, null=True,
        verbose_name = 'In regola?',)

    def get_full_name(self):
        return self.user.get_full_name()
    get_full_name.short_description = 'Nome'

    def get_thumb(self):
        if self.avatar:
            return FileObject(str(self.avatar))
        return

    def is_complete(self):
        no = format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
        yes = format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        if self.parent and self.gender:
            return yes
        elif self.sector == '0-NO' and self.user.first_name:
            return yes
        elif self.sector == '3-FI' and self.user.first_name and self.fiscal_code:
            return yes
        elif self.user.first_name and self.gender and self.phone:
            return yes
        else:
            return no
    is_complete.short_description = 'Completo'

    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if self.parent:
            mailto = [self.parent.email, ]
        else:
            mailto = [self.user.email, ]
        if self.mc_state == '02NI':
            self.mc_state = '04NN'
            mc_state_email(mailto, self.get_full_name(), 'inesistente')
        elif self.mc_state == '62II':
            self.mc_state = '64IN'
            mc_state_email(mailto, self.get_full_name(), 'in scadenza')
        elif self.mc_state == '4-SI':
            self.med_cert = None
            self.mc_expiry = None
            self.mc_state = '5-NI'
            mc_state_email(mailto, self.get_full_name(), 'scaduto')
        return super(Profile, self).save(*args, **kwargs)

    class Meta:
        ordering = ('user__last_name', 'user__first_name', 'user__username')
        verbose_name = 'Iscritto'
        verbose_name_plural = 'Iscritti'

class MemberPayment(models.Model):
    member = models.ForeignKey(Profile, on_delete = models.CASCADE,
        blank = True, null = True, related_name='member_payments')
    date = models.DateField( blank=True, null=True, verbose_name = 'Data')
    amount = models.FloatField( default = 0.00, verbose_name = 'Importo')

    def __str__(self):
        return 'Pagamento - %s' % (self.id)

    class Meta:
        ordering = ( '-date', )
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamenti'

class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='user_message', blank=True, null=True,
        verbose_name = 'Utente', )
    nickname = models.CharField(max_length = 50,
        verbose_name = 'Nome', blank=True, null=True,)
    email = models.EmailField(blank=True, null=True,
        verbose_name = 'Inviato da',)
    recipient = models.EmailField(blank=True, null=True,
        verbose_name = 'Destinatario')
    subject = models.CharField(max_length = 200,
        verbose_name = 'Soggetto', )
    body = models.TextField(verbose_name = 'Messaggio', )
    attachment = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Allegato',
        )
    privacy = models.BooleanField( default=False )

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return self.nickname
    get_full_name.short_description = 'Nome'

    def get_email(self):
        if self.user:
            return self.user.email
        else:
            return self.email
    get_email.short_description = 'Indirizzo email'

    def __str__(self):
        return 'Messaggio - %s' % (self.id)

    class Meta:
        verbose_name = 'Messaggio'
        verbose_name_plural = 'Messaggi'
