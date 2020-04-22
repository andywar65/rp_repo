from django.urls import path
from direzione.views import (ConventionListView, ConventionDetailView, )

app_name = 'conventions'

urlpatterns = [
    path('', ConventionListView.as_view(), name = 'index'),
    path('<slug>/', ConventionDetailView.as_view(), name = 'detail'),
    ]
