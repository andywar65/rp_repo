# Generated by Django 3.0.4 on 2020-03-30 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_stream_rendered'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='stream_search',
            field=models.TextField(editable=False, null=True),
        ),
    ]
