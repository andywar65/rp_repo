from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView,
    TemplateView)
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, DayArchiveView, )

from taggit.models import Tag

from .models import (Location, Event, )

class ListLocation(ListView):
    model = Location
    context_object_name = 'all_locations'
    paginate_by = 12

class DetailLocation(DetailView):
    model = Location
    context_object_name = 'location'
    slug_field = 'slug'

class TagMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        if 'categoria' in self.request.GET:
            context['tag_filter'] = self.request.GET['categoria']
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if 'categoria' in self.request.GET:
            qs = qs.filter(tags__name=self.request.GET['categoria'])
        return qs

class EventArchiveIndexView(TagMixin, ArchiveIndexView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    paginate_by = 12
    allow_empty = True

class EventYearArchiveView(TagMixin, YearArchiveView):
    model = Event
    make_object_list = True
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    paginate_by = 12
    year_format = '%Y'
    allow_empty = True

class EventMonthArchiveView(TagMixin, MonthArchiveView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    year_format = '%Y'
    month_format = '%m'
    allow_empty = True

class EventDayArchiveView(TagMixin, DayArchiveView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'
    allow_empty = True

class DetailEvent(DetailView):
    model = Event
    context_object_name = 'event'
    slug_field = 'slug'
