from django.urls import path
from .views import (RaceDetailView, RaceRedirectView, CorrectRedirectView,
    RaceListView, RaceListAthleteView)

app_name = 'criterium'
urlpatterns = [
    path('', RaceRedirectView.as_view(), name = 'all_editions'),
    path('<int:year>/', CorrectRedirectView.as_view(), name = 'correct_edition'),
    path('<int:year>-<int:year2>/', RaceListView.as_view(), name = 'edition'),
    path('<int:year>-<int:year2>/athlete/<int:id>',
        RaceListAthleteView.as_view(), name = 'athlete'),
    path('<int:year>-<int:year2>/<slug>/', RaceDetailView.as_view(), name = 'race'),
    ]
