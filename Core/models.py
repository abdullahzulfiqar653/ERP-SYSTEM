from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    subject, from_email, to = 'Password Reset Link by {}'.format(settings.SITE_NAME), settings.EMAIL_HOST_USER, reset_password_token.user.email
    text_content = 'This is an important message.'
    html_content = '<p>To reset your password kindly  <strong><a href="{}://{}{}?token={}">Click here.</a></strong></p>'.format(settings.PASSWORD_RESET_PROTOCOL, settings.PASSWORD_RESET_DOMAIN, reverse('password_reset:reset-password-request'), reset_password_token.key)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()