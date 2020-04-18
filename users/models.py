import os
from datetime import date, timedelta
from PIL import Image
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from filebrowser.fields import FileBrowseField
from filebrowser.base import FileObject
from .choices import SECTOR, GENDER, COURSE, NO_COURSE
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
        age = ( date.today() - self.profile.date_of_birth).days
        if age >= 18*365:
            return True
        return False

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
        verbose_name = 'Persona conosciuta',)

    def get_full_name(self):
        return self.user.get_full_name()
    get_full_name.short_description = 'Nome'

    def get_thumb(self):
        if self.avatar:
            return FileObject(str(self.avatar))
        return

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Profilo'
        verbose_name_plural = 'Profili'

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
