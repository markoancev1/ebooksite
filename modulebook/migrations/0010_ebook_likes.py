# Generated by Django 3.1.4 on 2020-12-17 22:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulebook', '0009_auto_20201215_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebook',
            name='likes',
            field=models.ManyToManyField(related_name='book_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
