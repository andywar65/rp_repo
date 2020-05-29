from django import forms
from django.forms import ModelForm
from .models import Society
from users.models import User

class SocietyForm(ModelForm):
    president = forms.ModelChoiceField(required = False,
        label = 'Presidente',
        queryset = User.objects.filter(profile__parent = None,
            is_active = True ), )
    executive = forms.ModelMultipleChoiceField(required = False,
        label = 'Dirigenti',
        queryset = User.objects.filter(profile__parent = None,
            is_active = True ), )
    trainers = forms.ModelMultipleChoiceField(required = False,
        label = 'Istruttori',
        queryset = User.objects.filter(profile__parent = None,
            is_active = True ), )

    class Meta:
        model = Society
        fields = '__all__'
