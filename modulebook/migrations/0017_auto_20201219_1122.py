# Generated by Django 3.1.4 on 2020-12-19 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulebook', '0016_auto_20201219_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]