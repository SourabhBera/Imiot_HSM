from django.core.mail import send_mail
from django.conf import settings


def send_IOE_email():
    subject = "Account Verification Email"
    message = f'Email received successfully.'
    email_from = settings.EMAIL_HOST_USER
    email_to = 'sourabhbera86@gmail.com'
    send_mail(subject, message, email_from, [email_to])
    return "\nEmail Sent!!"
