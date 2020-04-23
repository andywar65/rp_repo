from django import forms
from django.forms import ModelForm
from .models import Event
from users.models import User

class EventForm(ModelForm):
    manager = forms.ModelChoiceField(label="Responsabile", required = False,
        queryset = User.objects.with_perm('cronache.add_event').order_by('last_name',
        'first_name', 'username'), )

    class Meta:
        model = Event
        fields = '__all__'
