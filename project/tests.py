from django.test import TestCase
from django.urls import reverse

from streamblocks.models import IndexedParagraph
from blog.models import Article, UserUpload
from cronache.models import Event
from pages.models import TreePage
from users.models import User
from .utils import generate_unique_slug, generate_unique_username

class UtilsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Article.objects.create(title='Existing article',
            date = '2020-05-13 15:58:00+02')
        User.objects.create_user(username='uni_cum', password='P4s5W0r6')

    def test_generate_unique_slug(self):
        self.assertEqual(generate_unique_slug(Article, 'Article 7'),
            'article-7')

    def test_generate_unique_slug_modified(self):
        self.assertEqual(generate_unique_slug(Article, 'Existing article'),
            'existing-article-1')

    def test_generate_unique_username(self):
        self.assertEqual(generate_unique_username('uni cum'), 'uni_cum_1')

class SearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        IndexedParagraph.objects.create(id=77, title='Foo', body='Bar')
        usr = User.objects.create_user(username='odysseus',
            password='P4s5W0r6')
        article = Article.objects.create(title='Article 4',
            date = '2020-05-10 15:53:00+02',
            stream = '[{"unique_id":"4h7dps","model_name":"IndexedParagraph","id":77,"options":{}}]',
            )
        event = Event.objects.create(title='Event 4',
            date = '2020-05-10 15:53:00+02',
            stream = '[{"unique_id":"4h7dps","model_name":"IndexedParagraph","id":77,"options":{}}]',
            )
        UserUpload.objects.create(user=usr, post=article, event=event,
            body='Foo Bar?')
        TreePage.objects.create(title='Page 2', path = '0001', depth = 1,
            numchild = 0,
            stream = '[{"unique_id":"4h6dps","model_name":"IndexedParagraph","id":77,"options":{}}]',
            )

    def test_search_results_view_status_code(self):
        response = self.client.get('/search/?q=foo')
        self.assertEqual(response.status_code, 200)

    def test_search_results_view_template(self):
        response = self.client.get('/search/?q=foo')
        self.assertTemplateUsed(response, 'search_results.html')

    def test_search_results_view_context_success(self):
        response = self.client.get('/search/?q=foo')
        self.assertTrue(response.context['success'])

    def test_search_results_view_context_success_false(self):
        response = self.client.get('/search/?q=false')
        self.assertFalse(response.context['success'])

    def test_search_results_view_not_validating(self):
        response = self.client.get('/search/?q=')
        self.assertFalse(response.context['success'])

    def test_search_results_view_context_posts(self):
        article = Article.objects.filter(slug='article-4')
        response = self.client.get('/search/?q=foo')
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(response.context['all_blogs'], article,
            transform=lambda x: x)

    def test_search_results_view_context_events(self):
        event = Event.objects.filter(slug='event-4')
        response = self.client.get('/search/?q=foo')
        self.assertQuerysetEqual(response.context['all_events'], event,
            transform=lambda x: x)

    def test_search_results_view_context_uploads(self):
        article = Article.objects.filter(slug='article-4')
        response = self.client.get('/search/?q=foo')
        self.assertQuerysetEqual(response.context['all_uploads'], article,
            transform=lambda x: x)

    def test_search_results_view_context_pages(self):
        page = TreePage.objects.filter(slug='page-2')
        response = self.client.get('/search/?q=foo')
        self.assertQuerysetEqual(response.context['pages'], page,
            transform=lambda x: x)

    def test_search_results_view_context_uploads_events(self):
        event = Event.objects.filter(slug='event-4')
        response = self.client.get('/search/?q=foo')
        self.assertQuerysetEqual(response.context['evt_uploads'], event,
            transform=lambda x: x)
