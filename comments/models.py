from django.db import models
import datetime

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_edited(self):
        return self.updated_at > self.created_at + datetime.timedelta(seconds=1)

    def __str__(self):
        return f"Comment by {self.author.get_full_name() or self.author.email} on Post ID {self.post.id}"