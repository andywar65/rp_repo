from django.contrib import admin
from .models import Race, Athlete
from .forms import RaceForm, AthleteForm

class AthleteInline(admin.TabularInline):
    model = Athlete
    fields = ('member', 'points', 'placement', 'time')
    extra = 0
    form = AthleteForm

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_date', 'get_location', 'description', )
    list_filter = ('date', )
    inlines = [ AthleteInline, ]
    form = RaceForm
    autocomplete_fields = ['location', ]
