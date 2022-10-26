from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import Author

User = get_user_model()


class Manuscript(models.Model):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    MINOR = 'minor'
    MAJOR = 'major'
    NA = 'under process'

    STATUS = (
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (MINOR, 'Minor'),
        (MAJOR, 'Major'),
        (NA, 'under process'),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='manuscripts', null=True)
    title = models.CharField(max_length=100)

    abstract = models.TextField(max_length=300)
    keywords = models.TextField(default='')
    article_type = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default=NA)
    saved = models.BooleanField(default=False)
    # editor=
    file = models.FileField(upload_to='manuscripts/', null=True, blank=True)
    # editor_assigned_date = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
