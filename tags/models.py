from django.db import models

# Create your models here.
class Tag(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=70, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name