from django.contrib import admin
from django.conf import settings
from users.models import Profile
from blog.admin import UserUploadInline
from .models import ( Location, Event, )
from .forms import EventForm

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'get_gmap_link')
    readonly_fields = ('slug', )
    search_fields = ('title', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'notice')
    inlines = [ UserUploadInline ]
    search_fields = ('title', 'date', 'intro', )
    form = EventForm
    autocomplete_fields = ['location', ]

    fieldsets = (
        ('Galleria', {
            'classes': ('collapse',),
            'fields': ('carousel', ),
        }),
        (None, {
            'fields': ('title', 'date', 'location', 'intro')
        }),
        ('Lancio', {
            'classes': ('collapse',),
            'fields': ('stream', ),
        }),
        ('Aggiornamenti', {
            'classes': ('collapse',),
            'fields': ('upgrade_stream', ),
        }),
        ('Cronaca', {
            'classes': ('collapse',),
            'fields': ('chron_stream', ),
        }),
        ('Area riservata', {
            'classes': ('collapse',),
            'fields': ('restr_stream', ),
        }),
        (None, {
            'fields': ('manager', 'tags', 'notice')
        }),
    )
