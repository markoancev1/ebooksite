# Generated by Django 3.1.4 on 2020-12-19 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modulebook', '0021_auto_20201219_1948'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='name',
            new_name='user',
        ),
    ]
