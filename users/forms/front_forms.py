from datetime import datetime
from django import forms
from django.contrib.auth.forms import UsernameField
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget, CheckboxSelectMultiple
from captcha.fields import ReCaptchaField
from users.models import (Profile, User, )
from users.widgets import SmallClearableFileInput
from users.choices import SECTOR

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

class ProfileAddChildForm(ModelForm):
    first_name = forms.CharField( label = 'Nome', required = True,
        widget = forms.TextInput())
    last_name = forms.CharField( label = 'Cognome', required = True,
        widget = forms.TextInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', )

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
    date_of_birth = forms.DateField( input_formats=['%d/%m/%Y'], required=True,
        label='Data di nascita (gg/mm/aaaa)',
        widget=SelectDateWidget(years=range(datetime.now().year ,
        datetime.now().year-100, -1), attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ('fiscal_code', 'gender', 'date_of_birth', 'place_of_birth',
            'nationality')

class ProfileChangeAddressForm(ModelForm):
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
