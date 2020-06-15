from django.contrib import admin
from .models import Race, Athlete
from .forms import RaceForm, AthleteForm

class AthleteInline(admin.TabularInline):
    model = Athlete
    fields = ('user', 'points', 'placement', 'time')
    extra = 0
    form = AthleteForm

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_date', 'get_location', 'description', )
    list_filter = ('date', )
    inlines = [ AthleteInline, ]
    form = RaceForm
    autocomplete_fields = ['location', ]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if formsets: #are there inlines?
            obj = form.instance #the model admin object
            rcache = obj.racecache #the cache object
            athletes = formsets[0].cleaned_data #inline data (first inline)
            athl_list = []
            for athlete in athletes:
                athl_list.append({'user': athlete['user'].id,
                    'name': athlete['user'].get_full_name(),
                    'gender': athlete['user'].profile.gender,
                    'points': athlete['points']})
            rcache.cache = athl_list
            rcache.save()
