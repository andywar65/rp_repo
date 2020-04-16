from datetime import datetime
from django import forms
from django.contrib.auth import (password_validation, )
from django.contrib.auth.forms import (AuthenticationForm, UsernameField,
    PasswordResetForm, SetPasswordForm)
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget, CheckboxSelectMultiple
from captcha.fields import ReCaptchaField
from users.models import (Profile, User, UserMessage, CourseSchedule, )
from users.widgets import SmallClearableFileInput
from users.choices import SECTOR, GENDER, COURSE, NO_COURSE
from users.validators import validate_codice_fiscale

class RegistrationForm(ModelForm):
    username = UsernameField(label = 'Nome utente', required = True,
        widget=forms.TextInput(attrs={'autofocus': True, }))
    email = forms.EmailField(label = 'Email', required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    privacy = forms.BooleanField(label="Ho letto l'informativa sulla privacy",
        required=True)
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', )

class ContactLogForm(ModelForm):

    class Meta:
        model = UserMessage
        fields = ('user', 'email', 'subject', 'body', 'attachment', 'recipient')
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': "Scrivi qui il soggetto"}),
            'body': forms.Textarea(attrs={'placeholder': "Scrivi qui il messaggio"}),
            'attachment' : SmallClearableFileInput(),}

class ContactForm(ModelForm):
    nickname = forms.CharField(label = 'Nome', required = True,
        widget=forms.TextInput(attrs={'autofocus': True,}))
    email = forms.EmailField(label = 'Email', required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    privacy = forms.BooleanField(label="Ho letto l'informativa sulla privacy",
        required=True)

    captcha = ReCaptchaField()

    class Meta:
        model = UserMessage
        fields = ('nickname', 'email', 'subject', 'body', 'privacy')
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': "Scrivi qui il soggetto"}),
            'body': forms.Textarea(attrs={'placeholder': "Scrivi qui il messaggio"}),
            }

class FrontAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
        'class': 'form-control'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
            'class': 'form-control'}),
    )

    def clean(self):
        cd = super().clean()
        try:
            username = cd.get('username')
            user = User.objects.get(username = username)
            if user.member.parent:
                self.add_error(None, forms.ValidationError(
                    """I minori non possono effettuare il login autonomamente!
                    Il loro account è gestito dai genitori.""",
                    code='minor_no_login',
                ))
        except:
            pass

class FrontPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254, label='Email di registrazione',
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'class': 'form-control'})
    )

class FrontSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            'class': 'form-control'}),
        strip=False, label='Nuova password',
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False, label='Ripeti la nuova password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            'class': 'form-control'}),
    )

class FrontPasswordChangeForm(FrontSetPasswordForm):
    old_password = forms.CharField(
        strip=False, label='Vecchia password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
            'autofocus': True, 'class': 'form-control'}),
    )

class ProfileChangeForm(forms.Form):
    avatar = forms.FileField( required = False, widget = SmallClearableFileInput())
    first_name = forms.CharField( label = 'Nome', required = True,
        widget = forms.TextInput())
    last_name = forms.CharField( label = 'Cognome', required = True,
        widget = forms.TextInput())
    email = forms.EmailField(label = 'Email', required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    bio = forms.CharField( label = 'Breve biografia', required = False,
        widget = forms.Textarea(attrs={'placeholder': "Parlaci un po' di te"}) )
    yes_spam = forms.BooleanField( label="Mailing list", required = False,
        help_text = "Vuoi ricevere notifiche sui nuovi articoli ed eventi?")
    sector = forms.CharField( required=True, label='Corri con noi?',
        widget=forms.Select(choices = SECTOR, ),)

class ProfileChangeRegistryForm(ModelForm):
    gender = forms.CharField( required=True, label='Sesso',
        widget=forms.Select(choices = GENDER, ),)
    date_of_birth = forms.DateField( input_formats=['%d/%m/%Y'], required=True,
        label='Data di nascita (gg/mm/aaaa)',
        widget=SelectDateWidget(years=range(datetime.now().year ,
        datetime.now().year-100, -1), attrs={'class': 'form-control'}))
    place_of_birth = forms.CharField( label = 'Luogo di nascita',
        required = True, widget = forms.TextInput())
    nationality = forms.CharField( label = 'Nazionalità', required = True,
        widget = forms.TextInput())
    fiscal_code = forms.CharField(required=True, label='Codice fiscale',
        validators=[validate_codice_fiscale])

    class Meta:
        model = Profile
        fields = ('fiscal_code', 'gender', 'date_of_birth', 'place_of_birth',
            'nationality')

class ProfileChangeAddressForm(ModelForm):
    fiscal_code = forms.CharField(required=True, label='Codice fiscale',
        validators=[validate_codice_fiscale])
    address = forms.CharField( label = 'Indirizzo', required = True,
        widget = forms.TextInput(),
        help_text = 'Via/Piazza, civico, CAP, Città',)
    phone = forms.CharField( label = 'Numero di telefono', required = True,
        widget = forms.TextInput())
    email_2 = forms.EmailField(label = 'Email secondaria', required = False,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))

    class Meta:
        model = Profile
        fields = ('fiscal_code', 'address', 'phone', 'email_2', )

class ProfileChangeCourseForm(ModelForm):

    def clean(self):
        cd = super().clean()
        try:
            course = cd.get('course')
            course_alt = cd.get('course_alt')
            for sched in course:
                if sched.full == 'Altro' and course_alt == None:
                    self.add_error('course_alt', forms.ValidationError(
                        "Hai scelto 'Altro', quindi scrivi qualcosa!",
                        code='describe_course_alternative',
                    ))
        except:
            pass

    class Meta:
        model = Profile
        fields = ( 'course', 'course_alt', 'course_membership',
            'sign_up', 'privacy', 'med_cert', )
        widgets = {
            'sign_up' : SmallClearableFileInput(),
            'privacy' : SmallClearableFileInput(),
            'med_cert' : SmallClearableFileInput(),
            'course': CheckboxSelectMultiple(),
            }

class ProfileChangeNoCourseForm(ModelForm):

    class Meta:
        model = Profile
        fields = ( 'no_course_membership',
            'sign_up', 'privacy', 'med_cert', )
        widgets = {
            'sign_up' : SmallClearableFileInput(),
            'privacy' : SmallClearableFileInput(),
            'med_cert' : SmallClearableFileInput(),
            }

class ProfileDeleteForm(forms.Form):
    delete = forms.BooleanField( label="Cancella il profilo", required = True,
        help_text = """Seleziona per cancellare il profilo.""")
