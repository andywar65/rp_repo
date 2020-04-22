from django.contrib import admin
from .models import (Convention, Society, Institutional, )
from .forms import SocietyForm

@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_location', )
    autocomplete_fields = ['location', ]

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('title', )
    form = SocietyForm
    autocomplete_fields = ['location', ]

@admin.register(Institutional)
class InstitutionalAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')
