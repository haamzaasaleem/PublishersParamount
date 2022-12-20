from celery import shared_task

from .mail import *
from .utils import *
@shared_task()
def PdfMergerAndConverter(data,manuscript_id):
    return converting2Pdf(data,manuscript_id)

@shared_task()
def new_manuscript_email_task(title, to_email):
    return new_manuscript_email(title , to_email)


@shared_task()
def coAuthor_new_manuscript_email_task(title, to_email):
    return coAuthor_new_manuscript_email(title, to_email)
