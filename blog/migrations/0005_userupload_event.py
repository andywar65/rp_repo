# Generated by Django 3.0.5 on 2020-04-22 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cronache', '0001_initial'),
        ('blog', '0004_remove_article_stream_rendered'),
    ]

    operations = [
        migrations.AddField(
            model_name='userupload',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_uploads', to='cronache.Event'),
        ),
    ]
