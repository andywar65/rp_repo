from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, DetailView, TemplateView)
from .models import (Convention, Institutional, Society, )

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

class PrivacyTemplateView(TemplateView):
    template_name = 'direzione/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_page(context, '3-PR')
        context = get_society(context)
        return context

class MembershipTemplateView(TemplateView):
    template_name = 'direzione/membership.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_page(context, '1-IS')
        return context

class AboutTemplateView(TemplateView):
    template_name = 'direzione/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_page(context, '2-ST')
        context = get_society(context)
        return context

class InstructionsTemplateView(TemplateView):
    template_name = 'direzione/instructions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_page(context, '4-IN')
        return context
