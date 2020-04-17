from django import forms
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from users.models import UserMessage
from users.widgets import SmallClearableFileInput

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
