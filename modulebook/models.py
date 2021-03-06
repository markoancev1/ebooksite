from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class Ebook(models.Model):
    ebook_title = models.CharField(max_length=25, blank=False, unique=True)
    ebook_description = models.TextField(max_length=750)
    ebook_preview_image = models.ImageField(upload_to="images/")
    ebook_document = models.FileField(upload_to="books/")
    likes = models.ManyToManyField(User, related_name="likes")

    def get_absolute_url(self):
        return reverse('detail_book', kwargs={'pk': self.pk})

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.ebook_title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile/')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(Ebook, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    email = models.EmailField()
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
