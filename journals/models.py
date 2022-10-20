from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Journal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_editor_in_chief(self):
        return self.editorinchief
