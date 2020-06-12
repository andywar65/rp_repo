from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import (DetailView, RedirectView, ListView)

from .models import (Race, Athlete, )
from users.models import User

class RaceDetailView(DetailView):
    model = Race
    context_object_name = 'race'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = context['object']
        edition = race.get_edition()
        if edition != str(self.kwargs['year'])+'-'+str(self.kwargs['year2']):
            raise Http404("Wrong edition")
        athletes = Athlete.objects.filter(race_id=race.id)
        females = athletes.filter(user__profile__gender='F').order_by('-points',
            'placement', 'user__last_name', 'user__first_name')
        males = athletes.filter(user__profile__gender='M').order_by('-points',
            'placement', 'user__last_name', 'user__first_name')
        context['females'] = females
        context['males'] = males
        return context

class RaceListMixin:

    def get_queryset(self):
        year1 = self.kwargs['year']
        year2 = self.kwargs['year2']
        if year2 != year1+1:
            raise Http404("Edition years are not consecutive")
        qs = Race.objects.filter(date__gte = datetime(year1, 11, 1),
            date__lt = datetime(year2, 11, 1)).order_by('date')
        return qs

    def get_status(self, year):
        if datetime(year, 10, 31) > datetime.now():
            return 'provvisoria'
        return 'definitiva'

    def get_context_years(self, context):
        context['year']= self.kwargs['year']
        context['year2']= self.kwargs['year2']
        context['year0'] = context['year'] - 1
        context['year3'] = context['year2'] + 1
        context['status'] = self.get_status(context['year2'])
        return context

class RaceListAthleteView(RaceListMixin, ListView):
    model = Race
    ordering = ('date', )
    context_object_name = 'all_races'
    template_name = 'criterium/race_list_athlete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_context_years(context)
        user = get_object_or_404(User, id=self.kwargs['id'])
        context['name'] = user.get_full_name()
        context['id'] = user.id
        race_list = context['all_races'].values_list('id', flat = True)
        athletes = Athlete.objects.filter(race_id__in = race_list,
            user_id = context['id'])
        if athletes:
            first = athletes.first()
            race_dict = {}
            for race in context['all_races']:
                try:
                    athlete = athletes.get(race_id = race.id )
                    race_dict[race] = athlete.points
                except:
                    pass
            context['all_races'] = race_dict
        else:
            context['all_races'] = None
        return context

class RaceListView(RaceListMixin, ListView):
    model = Race
    ordering = ('date', )
    context_object_name = 'all_races'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_context_years(context)
        athl_list = []
        name_dict = {}
        fem_sums = {}
        male_sums = {}
        #get all athlete lists from race caches
        for race in context['all_races']:
            athl_list.extend(race.racecache.cache)
        #initialize point sums for each athlete
        for athl in athl_list:
            name_dict[athl['user']] = athl['name']
            if athl['gender'] == 'F':
                fem_sums[athl['user']] = 0
            else:
                male_sums[athl['user']] = 0
        #adding points to point sums
        for athl in athl_list:
            if athl['gender'] == 'F':
                fem_sums[athl['user']] += athl['points']
            else:
                male_sums[athl['user']] += athl['points']
        # thanks to https://stackoverflow.com/questions/613183/
        # how-do-i-sort-a-dictionary-by-value
        fem_sums = {k: v for k, v in sorted(fem_sums.items(),
            key=lambda item: item[1], reverse = True)}
        male_sums = {k: v for k, v in sorted(male_sums.items(),
            key=lambda item: item[1], reverse = True)}
        #adding names
        for id, point_sum in fem_sums.items():
            fem_sums[id] = (name_dict[id], point_sum)
        for id, point_sum in male_sums.items():
            male_sums[id] = (name_dict[id], point_sum)
        context['females'] = fem_sums
        context['males'] = male_sums
        return context

def get_edition_years():
    date = datetime.now()
    year = date.year
    month = date.month
    if month >= 11:
        year1 = year
        year2 = year + 1
    else:
        year1 = year - 1
        year2 = year
    return year1, year2

class RaceRedirectView(RedirectView):
    """redirects simple /criterium/ url to current edition url"""
    def get_redirect_url(self, *args, **kwargs):
        year1, year2 = get_edition_years()
        url = f'/criterium/{year1}-{year2}/'
        return url

class CorrectRedirectView(RedirectView):
    """redirects simple year url to double year url"""
    def get_redirect_url(self, *args, **kwargs):
        year = kwargs['year']
        url = f'/criterium/{year}-{year+1}/'
        return url
