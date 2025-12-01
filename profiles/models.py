from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    friends = models.ManyToManyField('users.User', related_name='friends', blank=True)

    def __str__(self):
        return f"Profile of {self.user.get_full_name() or self.user.email}"