from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Message from {self.sender.get_full_name() or self.sender.email} to {self.recipient.get_full_name() or self.recipient.email}'