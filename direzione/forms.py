from django import forms
from django.forms import ModelForm
from .models import Society
from users.models import Member

class SocietyForm(ModelForm):
    president = forms.ModelChoiceField(required = False,
        label = 'Presidente',
        queryset = Member.objects.filter(parent = None,
            user__is_active = True ), )
    executive = forms.ModelMultipleChoiceField(required = False,
        label = 'Dirigenti',
        queryset = Member.objects.filter(parent = None,
            user__is_active = True ), )
    trainers = forms.ModelMultipleChoiceField(required = False,
        label = 'Istruttori',
        queryset = Member.objects.filter(parent = None,
            user__is_active = True ), )

    class Meta:
        model = Society
        fields = '__all__'
