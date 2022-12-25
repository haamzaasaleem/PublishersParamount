from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail


def resetPasswordMailer(user, data):
    html_content = render_to_string("ForgotPasswordEmailtemplate.html",
                                    {'title': f'{user.username}', 'link': f'http://127.0.0.1:8000/{uuidToken}/'})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Password Reset Email - {user.username}',
        text_content,
        'haamzaasaleem@gmail.com',
        [f"{data}"]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return True


def userRegistrationMailer(user_data, profile_data):
    html_content = render_to_string("UserRegistrationMailer.html",
                                    {'data': f'{user_data}', 'link': f'http://127.0.0.1:8000/sign-in/'})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Successfully Registered - {user_data["username"]}',
        text_content,
        'haamzaasaleem@gmail.com',
        [f"{user_data['email']}"]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return True


def resetAuthPasswordMailer(user):
    html_content = render_to_string("resetAuthPasswordEmailer.html",
                                    {'title': f'{user.username}'})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Password Changed - {user.username}',
        text_content,
        'haamzaasaleem@gmail.com',
        [f"{user.email}"]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return True


def addReviewerMail(to_email, string):
    subject = 'Invited as a Reviewer'
    html_message = render_to_string('addReviewerMail.html', {'string': string})
    plain_message = strip_tags(html_message)
    from_email = 'haamzaasaleem@gmail.com'
    to = to_email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
