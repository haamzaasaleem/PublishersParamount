from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Journal(models.Model):
    title = models.CharField(max_length=100)
    issn_online = models.CharField(max_length=100, default=None)
    issn_print = models.CharField(max_length=100, default=None)
    doi = models.CharField(max_length=100, default=None)

    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    journal_image = models.ImageField(upload_to='journal_image/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_editor_in_chief(self):
        return self.editorinchief
