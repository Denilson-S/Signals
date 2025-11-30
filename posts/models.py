from django.db import models

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField('users.User', related_name='liked_posts', blank=True)
    shares = models.ManyToManyField('users.User', related_name='shared_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.get_full_name() or self.author.email