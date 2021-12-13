from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from ippanel import Client

from .models import Visitor

# @receiver(post_save, sender=Visitor)
# def send_greeting_test_message(sender, instance, created, *args, **kwargs):
#     if created:
#         client = Client(settings.IPPANEL_API_KEY)
#         client.send('9810004223', [instance.cellphone_number], "تست")
#         print("message sent")
