from django.db import models
from django.urls import reverse
# Create your models here.


class Ebook(models.Model):
    ebook_title = models.CharField(max_length=25, blank=False, unique=True)
    ebook_description = models.TextField(max_length=750)
    ebook_preview_image = models.ImageField(upload_to="images/")
    ebook_document = models.FileField(upload_to="books/")

    def __str__(self):
        return self.ebook_title

    def get_absolute_url(self):
        return reverse("albums:album-list", kwargs={"id": self.id})
