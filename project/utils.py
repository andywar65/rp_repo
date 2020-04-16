from django.utils.text import slugify
from users.models import User

def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug exists.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    Thanks to djangosnippets.org!
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug

def generate_unique_username(username):
    username = username.replace(' ', '_')
    unique_username = username
    numb = 1
    while User.objects.filter(username=unique_username).exists():
        unique_username = '%s_%d' % (username, numb)
        numb += 1
    return unique_username
