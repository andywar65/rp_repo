from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, DetailView, TemplateView)
from .models import (Convention, Society, )

class ConventionListView(ListView):
    model = Convention
    ordering = ('title', )
    context_object_name = 'all_conventions'
    paginate_by = 12

class ConventionDetailView(DetailView):
    model = Convention
    context_object_name = 'conv'
    slug_field = 'slug'

def get_page(context, type):
    page = get_object_or_404(Institutional, type=type)
    context['page'] = page
    return context

def get_society(context):
    try:
        context['society'] = Society.objects.get(title='Rifondazione Podistica')
    except:
        pass
    return context
