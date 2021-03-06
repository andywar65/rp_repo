"""project_repo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""WARNING:
    Commits to this file may not be cherry-picked by branches"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView

import private_storage.urls
from filebrowser.sites import site

from users.views import RegistrationFormView, ContactFormView
from pages.views import HomeTemplateView
from . import views

admin.site.site_header = 'Amministrazione ' + settings.WEBSITE_NAME
admin.site.site_title = 'Amministrazione ' + settings.WEBSITE_NAME

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('registration/', RegistrationFormView.as_view(),
        name='registration'),
    path('contacts/', ContactFormView.as_view(), name='contacts'),
    path('accounts/', include('users.urls')),
    path('search/', views.search_results, name='search_results'),
    path('', HomeTemplateView.as_view()),
    path('convenzioni/', include('direzione.urls.conventions',
        namespace = 'conventions')),
    path('calendario/', include('cronache.urls.events', namespace = 'chronicles')),
    path('luoghi/', include('cronache.urls.locations', namespace = 'locations')),
    path('archivio/', include('wordpress.urls', namespace = 'wordpress')),
    path('criterium/', include('criterium.urls', namespace = 'criterium')),
    path('articoli/', include('blog.urls.posts', namespace = 'blog')),
    path('docs/', include('pages.urls.tree_pages', namespace = 'docs')),
    path('streamfield/', include('streamfield.urls')),
    path('favicon.ico',
        RedirectView.as_view(url=settings.STATIC_ROOT + 'images/favicon.ico')),
    re_path('^private-media/', include(private_storage.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
