from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.models import Author

User = get_user_model()

def NewManuscriptMailer(manuscript, author):
    user = User.objects.get(id=author.user_id)
    html_content = render_to_string("ForgotPasswordEmailtemplate.html",
                                    {'title': f'{manuscript.title}'})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'New Manuscript Added - {author.first_name} {author.last_name}',
        text_content,
        'haamzaasaleem@gmail.com',
        [f"{user.email}"]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return True


def SaveManuscriptMailer(manuscript, author):
    author_obj = Author.objects.get(id=author)
    user = User.objects.get(id=author_obj.user_id)
    html_content = render_to_string("ForgotPasswordEmailtemplate.html",
                                    {'title': f'{manuscript.title}'})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Your Manuscript has been successfully Submitted - {author.first_name} {author.last_name}',
        text_content,
        'haamzaasaleem@gmail.com',
        [f"{user.email}"]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return True