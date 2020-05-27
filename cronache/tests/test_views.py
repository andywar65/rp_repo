from django.test import TestCase
from django.urls import reverse

from taggit.models import Tag

from users.models import User, Profile
from blog.models import Article, UserUpload
from cronache.models import Event, Location

class LocationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        tag = Tag.objects.create( name='bar' )
        #usr = User.objects.create_user(username='logged_in',
            #password='P4s5W0r6')
        #profile = Profile.objects.get(pk=usr.id)
        #profile.is_trusted = True
        #profile.save()
        #User.objects.create_user(username='untrusted', password='P4s5W0r6')
        #article = Article.objects.create(id=34, title='Article 3',
            #date = '2020-05-10 15:53:00+02', author = usr
            #)
        #article.tags.add('foo')
        #Article.objects.create(title='Article 4',
            #date = '2020-05-10 15:58:00+02')
        #UserUpload.objects.create(user=usr, post=article, body='Foo Bar')
        location = Location.objects.create(title='Where again', address='Mean St.',
            gmap_embed='http')
        event = Event.objects.create(title='Birthday party',
            date='2020-05-10 15:53:00+02', location=location)
        event.tags.add('bar')

    def test_locations_list_view_status_code(self):
        response = self.client.get(reverse('locations:locations'))
        self.assertEqual(response.status_code, 200)

    def test_locations_list_view_template(self):
        response = self.client.get(reverse('locations:locations'))
        self.assertTemplateUsed(response, 'cronache/location_list.html')

    def test_locations_list_view_context_object(self):
        all_locations = Location.objects.all()
        response = self.client.get(reverse('locations:locations'))
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(response.context['all_locations'],
            all_locations, transform=lambda x: x)

    def test_locations_detail_view_status_code(self):
        response = self.client.get(reverse('locations:location',
            kwargs={'slug': 'where-again'}))
        self.assertEqual(response.status_code, 200)

    def test_locations_detail_view_template(self):
        response = self.client.get(reverse('locations:location',
            kwargs={'slug': 'where-again'}))
        self.assertTemplateUsed(response, 'cronache/location_detail.html')

    def test_locations_detail_view_context_object(self):
        location = Location.objects.get(slug='where-again')
        response = self.client.get(reverse('locations:location',
            kwargs={'slug': 'where-again'}))
        self.assertEqual(response.context['location'], location )

    def test_event_archive_index_view_status_code(self):
        response = self.client.get(reverse('chronicles:event_index'))
        self.assertEqual(response.status_code, 200)

    def test_event_archive_index_view_template(self):
        response = self.client.get(reverse('chronicles:event_index'))
        self.assertTemplateUsed(response, 'cronache/event_archive.html')

    def test_event_archive_index_view_context_object(self):
        all_events = Event.objects.all()
        response = self.client.get(reverse('chronicles:event_index'))
        self.assertQuerysetEqual(response.context['all_events'],
            all_events, transform=lambda x: x)

    def test_event_archive_index_view_context_object_tagged(self):
        all_events = Event.objects.filter( tags__name='bar' )
        response = self.client.get('/calendario/?categoria=bar')
        self.assertQuerysetEqual(response.context['all_events'],
            all_events, transform=lambda x: x)

    #def test_article_year_archive_view_status_code(self):
        #response = self.client.get(reverse('blog:post_year',
            #kwargs={'year': 2020}))
        #self.assertEqual(response.status_code, 200)

    #def test_article_year_archive_view_template(self):
        #response = self.client.get(reverse('blog:post_year',
            #kwargs={'year': 2020}))
        #self.assertTemplateUsed(response, 'blog/article_archive_year.html')

    #def test_article_year_archive_view_context_object(self):
        #all_posts = Article.objects.filter(date__year=2020)
        #response = self.client.get(reverse('blog:post_year',
            #kwargs={'year': 2020}))
        #self.assertQuerysetEqual(response.context['posts'], all_posts,
            #transform=lambda x: x)

    #def test_article_month_archive_view_status_code(self):
        #response = self.client.get(reverse('blog:post_month',
            #kwargs={'year': 2020, 'month': 5}))
        #self.assertEqual(response.status_code, 200)

    #def test_article_month_archive_view_template(self):
        #response = self.client.get(reverse('blog:post_month',
            #kwargs={'year': 2020, 'month': 5}))
        #self.assertTemplateUsed(response, 'blog/article_archive_month.html')

    #def test_article_month_archive_view_context_object(self):
        #all_posts = Article.objects.filter(date__year=2020, date__month=5)
        #response = self.client.get(reverse('blog:post_month',
            #kwargs={'year': 2020, 'month': 5}))
        #self.assertQuerysetEqual(response.context['posts'], all_posts,
            #transform=lambda x: x)

    #def test_article_day_archive_view_status_code(self):
        #response = self.client.get(reverse('blog:post_day',
            #kwargs={'year': 2020, 'month': 5, 'day': 10}))
        #self.assertEqual(response.status_code, 200)

    #def test_article_day_archive_view_template(self):
        #response = self.client.get(reverse('blog:post_day',
            #kwargs={'year': 2020, 'month': 5, 'day': 10}))
        #self.assertTemplateUsed(response, 'blog/article_archive_day.html')

    #def test_article_day_archive_view_context_object(self):
        #all_posts = Article.objects.filter(date__year=2020, date__month=5,
            #date__day=10)
        #response = self.client.get(reverse('blog:post_day',
            #kwargs={'year': 2020, 'month': 5, 'day': 10}))
        #self.assertQuerysetEqual(response.context['posts'], all_posts,
            #transform=lambda x: x)

    #def test_article_detail_view_status_code(self):
        #response = self.client.get(reverse('blog:post_detail',
            #kwargs={'year': 2020, 'month': 5, 'day': 10, 'slug': 'article-3'}))
        #self.assertEqual(response.status_code, 200)

    #def test_article_detail_view_template(self):
        #response = self.client.get(reverse('blog:post_detail',
            #kwargs={'year': 2020, 'month': 5, 'day': 10, 'slug': 'article-3'}))
        #self.assertTemplateUsed(response, 'blog/article_detail.html')

    #def test_article_detail_view_context_object(self):
        #article = Article.objects.get(slug='article-3')
        #response = self.client.get(reverse('blog:post_detail',
            #kwargs={'year': 2020, 'month': 5, 'day': 10, 'slug': 'article-3'}))
        #self.assertEqual(response.context['post'], article )

    #def test_author_list_view_status_code(self):
        #response = self.client.get(reverse('blog:post_authors'))
        #self.assertEqual(response.status_code, 200)

    #def test_author_list_view_template(self):
        #response = self.client.get(reverse('blog:post_authors'))
        #self.assertTemplateUsed(response, 'blog/author_list.html')

    #def test_author_list_view_context_object(self):
        #all_users = User.objects.all()
        #response = self.client.get(reverse('blog:post_authors'))
        #self.assertQuerysetEqual(response.context['user_list'], all_users,
            #transform=lambda x: x )

    #def test_author_list_view_context_authors(self):
        #usr = User.objects.get(username='logged_in')
        #response = self.client.get(reverse('blog:post_authors'))
        #here we have only one author
        #self.assertEqual(response.context['authors'], {usr: (1,1)} )

    #def test_by_author_list_view_status_code(self):
        #usr = User.objects.get(username='logged_in')
        #response = self.client.get(reverse('blog:post_by_author',
            #kwargs={ 'pk' : usr.id }))
        #self.assertEqual(response.status_code, 200)

    #def test_by_author_list_view_template(self):
        #usr = User.objects.get(username='logged_in')
        #response = self.client.get(reverse('blog:post_by_author',
            #kwargs={ 'pk' : usr.id }))
        #self.assertTemplateUsed(response, 'blog/article_archive_authors.html')

    #def test_by_author_list_view_context_object(self):
        #usr = User.objects.get(username='logged_in')
        #posts = Article.objects.filter( author_id=usr.id )
        #response = self.client.get(reverse('blog:post_by_author',
            #kwargs={ 'pk' : usr.id }))
        #self.assertQuerysetEqual(response.context['posts'], posts,
            #transform=lambda x: x )

    #def test_by_author_list_view_context_object_tagged(self):
        #usr = User.objects.get(username='logged_in')
        #posts = Article.objects.filter( author_id=usr.id, tags__name='foo' )
        #response = self.client.get(f'/articoli/autori/{usr.id}/?tag=foo')
        #self.assertQuerysetEqual(response.context['posts'], posts,
            #transform=lambda x: x )

    #def test_by_upload_list_view_status_code(self):
        #usr = User.objects.get(username='logged_in')
        #response = self.client.get(reverse('blog:upload_by_author',
            #kwargs={ 'pk' : usr.id }))
        #self.assertEqual(response.status_code, 200)

    #def test_by_upload_list_view_template(self):
        #usr = User.objects.get(username='logged_in')
        #response = self.client.get(reverse('blog:upload_by_author',
            #kwargs={ 'pk' : usr.id }))
        #self.assertTemplateUsed(response, 'blog/uploads_by_author.html')

    #def test_by_upload_list_view_context_object(self):
        #usr = User.objects.get(username='logged_in')
        #uploads = UserUpload.objects.filter( user_id=usr.id )
        #response = self.client.get(reverse('blog:upload_by_author',
            #kwargs={ 'pk' : usr.id }))
        #self.assertQuerysetEqual(response.context['uploads'], uploads,
            #transform=lambda x: x )

    #def test_user_upload_create_view_redirect_not_logged(self):
        #response = self.client.get('/articoli/contributi/?post_id=34')
        #self.assertRedirects(response,
            #'/accounts/login/?next=/articoli/contributi/%3Fpost_id%3D34')

    #def test_user_upload_create_view_status_code(self):
        #self.client.post('/accounts/login/', {'username':'logged_in',
            #'password':'P4s5W0r6'})
        #response = self.client.get(reverse('blog:post_upload'))
        #self.assertEqual(response.status_code, 200)

    #def test_user_upload_create_view_untrusted_status_code(self):
        #self.client.post('/accounts/login/', {'username':'untrusted',
            #'password':'P4s5W0r6'})
        #response = self.client.get(reverse('blog:post_upload'))
        #self.assertEqual(response.status_code, 404)

    #def test_user_upload_create_view_template(self):
        #self.client.post('/accounts/login/', {'username':'logged_in',
            #'password':'P4s5W0r6'})
        #response = self.client.get(reverse('blog:post_upload'))
        #self.assertTemplateUsed(response, 'blog/userupload_form.html')

    #def test_user_upload_create_view_success_url(self):
        #self.client.post('/accounts/login/',# {'username':'logged_in',
            #'password':'P4s5W0r6'})
        #response = self.client.post('/articoli/contributi/?post_id=34',
            #{'body': 'Foo Bar'})
        #self.assertRedirects(response,
            #'/articoli/2020/05/10/article-3/#upload-anchor')

    #def test_user_upload_create_view_event_success_url(self):
        #self.client.post('/accounts/login/', {'username':'logged_in',
            #'password':'P4s5W0r6'})
        #event = Event.objects.get(slug='birthday')
        #response = self.client.post(f'/articoli/contributi/?event_id={event.id}',
            #{'body': 'Foo Bar'})
        #self.assertRedirects(response,
            #'/calendario/2020/05/10/birthday/#upload-anchor')
