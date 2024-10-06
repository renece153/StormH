from django.db import models

# Create your models here.


class UserEmail(models.Model):
    # By default, Django adds an `id` field which is an auto-incrementing primary key.
    email = models.EmailField(unique=True)  # Unique email field
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation

    def __str__(self):
        return self.email


class ChatMessage(models.Model):
    user_email = models.ForeignKey(UserEmail, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email}: {self.message}"

        