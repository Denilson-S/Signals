from django.db import models
import datetime

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.ManyToManyField('tags.Tag', related_name='tagged_posts', blank=True)
    likes = models.ManyToManyField('users.User', related_name='liked_posts', blank=True)
    shares = models.ManyToManyField('users.User', related_name='shared_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_edited(self):
        return self.updated_at > self.created_at + datetime.timedelta(seconds=1)

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'