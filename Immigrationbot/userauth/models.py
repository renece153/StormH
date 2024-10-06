from django.db import models

# Create your models here.


class UserEmail(models.Model):
    # By default, Django adds an `id` field which is an auto-incrementing primary key.
    email = models.EmailField(unique=True)  # Unique email field
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation

    def __str__(self):
        return self.email
