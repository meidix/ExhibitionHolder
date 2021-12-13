from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from ippanel import Client

from .models import Visitor

# @receiver(post_save, sender=Visitor)
# def send_greeting_test_message(sender, instance, created, *args, **kwargs):
#     if created:
#         client = Client(settings.IPPANEL_API_KEY)
#         client.send('9810004223', [instance.cellphone_number], "تست")
#         print("message sent")

# @receiver(post_save, sender=Visitor)
# def send_visitor_data(sender, instance, created, *args, **kwargs):
#     if created:
#         context = {
#             "visitor": instance,
#             'coops': instance.coop_request.all(),
#             'products': instance.products_request.all(),
#         }
#         subject = f'بازدید کننده جدید در {instance.exhibition.title}'
#         html_message = render_to_string('exhibitions/report.html', context=context)
#         plain_message = strip_tags(html_message)
#         to = 'mahdihossieni@gmail.com'
#         send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [to], fail_silently=True, html_message=html_message)
