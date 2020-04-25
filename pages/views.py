from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from streamblocks.models import HomeButton

from blog.models import Article
from cronache.models import Event
from direzione.models import Society
from .models import ( HomePage, TreePage )

class HomeTemplateView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = HomePage.objects.first()
        if not context['page']:
            raise Http404("Non ci sono Home Page")
        context['all_events'] = Event.objects.all()[:6]
        context['posts'] = Article.objects.all()[:6]
        actions = context['page'].action.from_json()
        for action in actions:
            context['actions'] = HomeButton.objects.filter(id__in = action['id'])[:3]
        return context

class TreePageListView(ListView):
    model = TreePage
    context_object_name = 'annotated_list'
    template_name = 'pages/tree_page_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['annotated_lists'] = []
        root_pages = TreePage.get_root_nodes()
        for root_page in root_pages:
            context['annotated_lists'].append(TreePage.get_annotated_list(parent=root_page))
        return context

class TreePageDetailView(DetailView):
    model = TreePage
    context_object_name = 'page'
    slug_field = 'slug'
    template_name = 'pages/tree_page.html'

    def get_context_data(self, **kwargs):
        if not self.object.get_path() == self.request.path:
            raise Http404("Il request path non corrisponde al get path")
        context = super().get_context_data(**kwargs)
        context['adjacent'] = self.object.get_adjacent_pages()
        if self.kwargs['slug'] == 'dati-societari':
            context['society'] = get_object_or_404(Society,
                title = 'Rifondazione Podistica')
        return context

    def get_template_names(self):
        if self.kwargs['slug'] == 'dati-societari':
            return 'pages/society_page.html'
        return super(TreePageDetailView, self).get_template_names()

#unable to use class based view!
def page_by_path(request, path):
    path_list = path.split('/')
    #last element may be trailing slash
    while not path_list.pop():
        last = path_list.pop()
    page = get_object_or_404( TreePage, slug = last )
    if not page.get_path() == request.path:
        raise Http404("Il request path non corrisponde al get path")
    adjacent = page.get_adjacent_pages()
    return render(request, 'pages/tree_page.html', { 'page': page,
        'adjacent': adjacent, })
