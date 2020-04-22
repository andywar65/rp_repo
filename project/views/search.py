from django import forms
from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from blog.models import Article, UserUpload
from pages.models import TreePage

class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)

def search_results(request):
    success = False
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = SearchQuery(request.GET['q'])
        #search in uploads
        v = SearchVector('body')
        uploads = UserUpload.objects.annotate(rank=SearchRank(v, q))
        #search in articles by upload
        art_uploads = uploads.filter(rank__gt=0.01).values_list('post_id',
            flat = True)
        article_uploads = Article.objects.filter(id__in = art_uploads)
        if article_uploads:
            success = True
        #search in articles
        v = SearchVector('title', 'intro', 'stream_search')
        articles = Article.objects.annotate(rank=SearchRank(v, q))
        articles = articles.filter(rank__gt=0.01)
        if articles:
            articles = articles.order_by('-rank')
            success = True
        #search in events by upload
        evt_uploads = uploads.filter(rank__gt=0.01).values_list('event_id',
            flat = True)
        event_uploads = Event.objects.filter(id__in = evt_uploads)
        if event_uploads:
            success = True
        #search in events
        v = SearchVector('title', 'intro', 'stream_search')
        events = Event.objects.annotate(rank=SearchRank(v, q))
        events = events.filter(rank__gt=0.01)
        if events:
            events = events.order_by('-rank')
            success = True
        #search in pages
        #v = SearchVector('title', 'intro', 'stream_rendered')
        pages = TreePage.objects.annotate(rank=SearchRank(v, q))
        pages = pages.filter(rank__gt=0.01)
        if pages:
            pages = pages.order_by('-rank')
            success = True
        return render(request, 'search_results.html',
            {'search': request.GET['q'], 'all_uploads': article_uploads,
            'all_blogs': articles, 'all_events': events,
            'evt_uploads': event_uploads, 'pages': pages, 'success': success})
    else:
        return render(request, 'search_results.html', {'success': success, })
