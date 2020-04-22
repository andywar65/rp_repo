import re
import sys
from datetime import datetime
import requests
from django.conf import settings
from django.views.generic import (TemplateView, )
from django.shortcuts import render
if not sys.version_info[:2] == (3,7):
    from backports.datetime_fromisoformat import MonkeyPatch
    MonkeyPatch.patch_fromisoformat()

target = settings.REST_API_TARGET

def get_user_name(id):
    response = requests.get(target + 'users/' + str(id) )
    author = response.json()
    return author['name']

def get_category_name(id):
    response = requests.get(target + 'categories/' + str(id) )
    category = response.json()
    return category['name']

def get_category_dict():
    response = requests.get(target + 'categories/', params = {'per_page': 100})
    all_cat = response.json()
    category_dict = {}
    for cat in all_cat:
        category_dict[cat['id']] = cat['name']
    return category_dict


def wp_list_view(request, category=None):
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    filter = {
        'categories': category,
        '_fields': 'id,title,excerpt,jetpack_featured_media_url',
        'per_page': 9,
        'page': page,
        }
    response = requests.get(target + 'posts', params = filter )
    wp_posts = response.json()
    if category:
        category = get_category_name(category)
    posts = []
    for wp_post in wp_posts:
        post = {}
        post['id'] = wp_post['id']
        post['title'] = wp_post['title']['rendered']
        excerpt = wp_post['excerpt']['rendered']
        post['excerpt'] = re.sub('<div class="sharedaddy.*</div></div></div>',
            '', excerpt)
        if wp_post['excerpt']['protected'] == True:
            post['visible'] = False
        else:
            post['visible'] = True
        post['image'] = wp_post['jetpack_featured_media_url']
        posts.append(post)
    return render(request, 'wordpress/wp_list.html', {'posts': posts, 'page': page,
    'previous': page-1, 'next': page+1, 'category': category,
    })

def wp_detail_view(request, id):
    filter = {
        #'id': id,
        '_fields': 'title,content,jetpack_featured_media_url,date,author,categories',
        }
    response = requests.get(target + 'posts/' + str(id), params = filter )
    wp_post = response.json()
    post = {}
    post['title'] = wp_post['title']['rendered']
    post['date'] = datetime.fromisoformat(wp_post['date'])
    if wp_post['author']:
        post['author'] = get_user_name(wp_post['author'])
    if wp_post['categories']:
        categories = {}
        category_dict = get_category_dict()
        for cat in wp_post['categories']:
            categories[cat] = category_dict[cat]
            post['categories'] = categories
    content = wp_post['content']['rendered']
    post['content'] = re.sub('<div class="sharedaddy.*</div></div></div>', '',
        content)
    if wp_post['content']['protected'] == True:
        post['visible'] = False
    else:
        post['visible'] = True
    post['image'] = wp_post['jetpack_featured_media_url']
    return render(request, 'wordpress/wp_detail.html', {'post': post,
    })

class CategoryTemplateView(TemplateView):
    template_name = 'wordpress/wp_category.html'
