# Generated by Django 3.1.4 on 2020-12-08 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulebook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='ebook_description',
            field=models.TextField(max_length=1000),
        ),
    ]
