from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


'''This method has 4 parameter. first for the content we need to write in Email and 2nd
is the subject of the email and 3rd is an email that whom we want to send the email and
4th one is the template that which type of email template will be used.'''
def send_email( email, subject, to_email, templateName):
    html_content = render_to_string("core/"+templateName, {'subject': subject, 'content': email})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER , ['abdullah@beyonderissolutions.com',]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()