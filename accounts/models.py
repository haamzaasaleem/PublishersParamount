from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'admin'
    STAFF = 'staff'
    AUTHOR = 'author'
    REVIEWER = 'reviewer'
    EDITOR = 'editor'
    EIC = 'eic'
    
    ROLES = (
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (AUTHOR, 'Author'),
        (REVIEWER, 'Reviewer'),
        (EDITOR, 'Editor'),
        (EIC, 'Editor in Chief'),
    )

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    role = models.CharField(choices=ROLES, max_length=50, default=AUTHOR)
    gender = models.CharField(choices=GENDER, max_length=100, default=MALE)
    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} [{self.get_role_display()}]"


class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} [{self.user.get_role_display()}]"

    class Meta:
        abstract = True


class Author(BaseProfile):

    def __str__(self):
        return f"{self.user.username} [{self.user.get_role_display()}]"

    def get_manuscripts(self):
        return self.manuscripts.all()


class EditorInChief(BaseProfile):
    journal = models.OneToOneField('journals.Journal', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} [{self.user.get_role_display()}]"


class Editor(BaseProfile):
    eic = models.OneToOneField(EditorInChief, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} [{self.user.get_role_display()}]"
