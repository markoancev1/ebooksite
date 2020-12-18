# Generated by Django 3.1.4 on 2020-12-18 00:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulebook', '0012_ebook_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
