from django import forms
from django.forms import ModelForm
from .models import UserUpload, Article
from users.models import User

class UserUploadForm(ModelForm):
    body = forms.CharField(label = 'Testo',
        widget=forms.Textarea(attrs={'placeholder': "Scrivi qui il messaggio"}))
    class Meta:
        model = UserUpload
        fields = ('image', 'body',)

class ArticleForm(ModelForm):
    author = forms.ModelChoiceField(label="Autore", required = False,
        queryset = User.objects.with_perm('blog.view_article').order_by('last_name',
        'first_name', 'username'), )

    class Meta:
        model = Article
        fields = '__all__'
