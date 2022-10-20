from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import Author

User = get_user_model()


class Manuscript(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='manuscripts', null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='manuscripts/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
