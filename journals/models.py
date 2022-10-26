from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Journal(models.Model):
    title = models.CharField(max_length=100)
    issn_online = models.CharField(max_length=100, default=None)
    issn_print = models.CharField(max_length=100, default=None)
    doi = models.CharField(max_length=100, default=None)

    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    journal_image = models.ImageField(upload_to='journal_image/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_editor_in_chief(self):
        return self.editorinchief
