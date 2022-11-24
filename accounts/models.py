from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from journals.models import Journal


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class User(AbstractUser):
    ADMIN = 'admin'
    STAFF = 'staff'
    AUTHOR = 'author'
    REVIEWER = 'reviewer'
    EDITOR = 'editor'
    EIC = 'eic'
    EIC_STAFF = 'eic_staff'
    E_STAFF = 'e_staff'

    ROLES = (
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (AUTHOR, 'Author'),
        (REVIEWER, 'Reviewer'),
        (EDITOR, 'Editor'),
        (EIC, 'Editor in Chief'),
        (EIC_STAFF, 'Eic Staff'),
        (E_STAFF, 'Editor Staff'),
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} [{self.get_role_display()}]"

class ForgetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)

class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True, default='/user_image/placeholder.jpeg')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
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


class Reviewer(BaseProfile):
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, null=True)
    keywords = models.CharField(max_length=5000, null=True, blank=True)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} [{self.user.get_role_display()}]"


class EicStaff(BaseProfile):
    eic = models.ForeignKey(EditorInChief, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} [{self.user.get_role_display()}]"


class EditorStaff(BaseProfile):
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, related_name='manuscripts', null=True)

    def __str__(self):
        return f"{self.user.username} [{self.user.get_role_display()}]"

