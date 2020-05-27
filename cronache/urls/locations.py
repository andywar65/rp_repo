from django.urls import path
from cronache.views import ListLocation, DetailLocation

app_name = 'locations'

urlpatterns = [
    path('', ListLocation.as_view(), name='locations'),
    path('<slug>/', DetailLocation.as_view(), name='location'),
    ]
