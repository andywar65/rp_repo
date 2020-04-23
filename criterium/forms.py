from django import forms
from django.forms import ModelForm
from .models import Race, Athlete
from cronache.models import Event
from users.models import Profile

class RaceForm(ModelForm):
    event = forms.ModelChoiceField(label="Evento", required = False,
        queryset = Event.objects.filter(tags__name__in = ['criterium',
        'Criterium'], ), )

    def clean_date(self):
        date = self.cleaned_data['date']
        event = self.cleaned_data['event']
        if not date and not event:
            msg = 'Senza evento occorre inserire almeno la data.'
            raise forms.ValidationError(msg)
        return date

    class Meta:
        model = Race
        fields = '__all__'

class AthleteForm(ModelForm):
    member = forms.ModelChoiceField(label="Iscritto", required = True,
        queryset = Profile.objects.filter(parent = None,
            sector__in = ['1-YC', '2-NC'],
            user__is_active = True ).order_by('user__last_name',
            'user__first_name'), )

    class Meta:
        model = Athlete
        fields = '__all__'
