from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from users.models import User
from .models import Profile
import os

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_delete, sender=Profile)
def delete_profile_avatar_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `Profile` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

@receiver(pre_save, sender=Profile)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem when corresponding `Profile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_avatar = Profile.objects.get(pk=instance.pk).avatar
    except Profile.DoesNotExist:
        return False

    new_avatar = instance.avatar
    if old_avatar and old_avatar != new_avatar:
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)
