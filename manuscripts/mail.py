from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def new_manuscript_email(title, to_email):
    subject = 'New Manuscript'
    html_message = render_to_string('NewManuscriptMailer.html', {'context': f'{title}'})
    plain_message = strip_tags(html_message)
    from_email = 'haamzaasaleem@gmail.com'
    to = to_email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def coAuthor_new_manuscript_email(title, to_email):
    subject = 'Added as a Co Author'
    html_message = render_to_string('CoAuthorNewManuscriptMailer.html', {'context': f'{title}'})
    plain_message = strip_tags(html_message)
    from_email = 'haamzaasaleem@gmail.com'
    to = to_email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def addReviewerMail(to_email):
    subject = 'Invited as a Reviewer'
    html_message = render_to_string('addReviewerMail.html')
    plain_message = strip_tags(html_message)
    from_email = 'haamzaasaleem@gmail.com'
    to = to_email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
